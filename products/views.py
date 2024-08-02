from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Tag, Product, Picture
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import ProductSerializer
from store.models import Store
from inventory.models import Inventory
import logging
from django.contrib.auth.decorators import login_required
from analytics.models import Analytic
from reviews.models import Review, Rating
from django.db.models import OuterRef, Subquery

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        store_id = self.request.data.get('store')
        store = get_object_or_404(Store, id=store_id, owner=self.request.user)
        serializer.save(store=store)
        
@login_required(login_url='login')
def create_product(request, store_name):
    if not request.user.is_authenticated:
        return redirect('/users/login/')
    
    store = get_object_or_404(Store, name=store_name, owner=request.user)

    if request.method == 'POST':
        logger.debug(f"POST data: {request.POST}")
        logger.debug(f"FILES: {request.FILES}")

        product_form = ProductForm(request.POST, request.FILES)
        tags = request.POST.get('tags', '').split(',')
        main_image_filename = request.POST.get('main_image', '')

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.store = store
            product.save()
            product_form.save_m2m()

            inventory = Inventory.objects.create(
                product=product,
                quantity=product_form.cleaned_data['quantity'],
                low_stock_threshold=product_form.cleaned_data['low_stock_threshold']
            )
            
            images = request.FILES.getlist('images')
            logger.debug(f"Images received: {images}")
            main_image_set = False

            for index, image in enumerate(images):
                is_main_image = False
                if main_image_filename and image.name == main_image_filename:
                    is_main_image = True
                elif not main_image_filename and index == 0:
                    is_main_image = True
                picture = Picture.objects.create(product=product, image=image, main=is_main_image)
                if is_main_image:
                    main_image_set = True

            if not main_image_set and images:
                first_picture = Picture.objects.filter(product=product).first()
                if first_picture:
                    first_picture.main = True
                    first_picture.save()

            for tag_name in tags:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    product.tags.add(tag)

            product.save()
            return redirect('my-stores')
    else:
        product_form = ProductForm()
        user_stores = Store.objects.filter(owner=request.user)

    return render(request, 'create_product.html', {
        'product_form': product_form,
        'user_stores': user_stores,
        'authenticated': request.user.is_authenticated,
        'store_name': store_name,
    })

def product_detail(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    inventory = get_object_or_404(Inventory, product=product)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    ratings = Rating.objects.filter(product=product)
    if request.user.is_authenticated:
        user_has_rated = Rating.objects.filter(product=product, user=request.user).exists()
        user_has_reviewed = Review.objects.filter(product=product, user=request.user).exists()
    else:
        user_has_rated = False
        user_has_reviewed = False
    stars = range(1, 6)
    main_image = product.pictures.filter(main=True).first()

    if not reviews.exists():
        reviews = None
    else:
        reviews = reviews[:3]
        review_ratings = Rating.objects.filter(product=product, user=OuterRef('user'))
        reviews = reviews.annotate(rating=Subquery(review_ratings.values('rating')[:1]))

    if not ratings.exists():
        rating = None
    else:
        rating = int((sum(rating.rating for rating in ratings) / len(ratings)) + .5)

    stop_words = set([
        "a", "and", "is", "it", "this", "the", "of", "in", "to", "with", "for", "on", "at",
        "by", "from", "an", "or", "as", "but", "not", "be", "are", "has", "have", "had",
        "that", "which", "who", "whom", "whose", "where", "when", "why", "how", "there", "here", "&"
    ])

    if product and request.user.is_authenticated:
        words = set(word for word in (product.name + " " + product.description + " " + product.category.name).lower().split() if word not in stop_words)
        tags = product.tags.all()

        for word in words:
            tag, created = Tag.objects.get_or_create(name=word)
            if created:
                tags.add(tag)

        for tag in tags:
            analytic, created = Analytic.objects.get_or_create(tag=tag, user=request.user)
            analytic.views += 1
            analytic.save()

    return render(request, 'product_detail.html', {
        'product': product,
        'inventory': inventory,
        'authenticated': request.user.is_authenticated,
        'rating': rating,
        'reviews': reviews,
        'stars': stars,
        'has_rated': user_has_rated,
        'has_reviewed': user_has_reviewed,
        'main_image': main_image.image.url,
    })


    
@login_required(login_url='login')
def edit_product(request, store_name, product_id):
    store = get_object_or_404(Store, name=store_name, owner=request.user)
    product = get_object_or_404(Product, id=product_id, store=store)

    if request.method == 'POST':
        logger.debug(f"POST data: {request.POST}")
        logger.debug(f"FILES: {request.FILES}")

        product_form = ProductForm(request.POST, request.FILES, instance=product)
        tags = request.POST.get('tags', '').split(',')
        main_image_filename = request.POST.get('main_image', '')

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.store = store
            product.save()
            product_form.save_m2m()

            inventory = Inventory.objects.get(product=product)
            inventory.quantity = product_form.cleaned_data['quantity']
            inventory.low_stock_threshold = product_form.cleaned_data['low_stock_threshold']
            inventory.save()
            
            images = request.FILES.getlist('images')
            logger.debug(f"Images received: {images}")
            main_image_set = False

            if images:
                product.pictures.all().delete()
                for index, image in enumerate(images):
                    is_main_image = False
                    if main_image_filename and image.name == main_image_filename:
                        is_main_image = True
                    elif not main_image_filename and index == 0:
                        is_main_image = True
                    picture = Picture.objects.create(product=product, image=image, main=is_main_image)
                    if is_main_image:
                        main_image_set = True

                if not main_image_set and images:
                    first_picture = Picture.objects.filter(product=product).first()
                    if first_picture:
                        first_picture.main = True
                        first_picture.save()

            for tag_name in tags:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    product.tags.add(tag)

            product.save()
            return redirect('my-stores', store_name=store.name)
    else:
        product_form = ProductForm(instance=product)
        user_stores = Store.objects.filter(owner=request.user)

    return render(request, 'edit_product.html', {
        'product_form': product_form,
        'user_stores': user_stores,
        'authenticated': request.user.is_authenticated,
        'product': product,
    })
