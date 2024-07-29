from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import ProductForm
from .models import Tag, Product
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import ProductSerializer
from store.models import Store

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(store=self.request.GET('store'))

def create_product(request):
    if not request.user.is_authenticated:
        return redirect('/users/login/')
    
    if request.method == 'POST':
        store_id = request.POST.get('store')
        store = get_object_or_404(Store, id=store_id, owner=request.user)
        
        product_form = ProductForm(request.POST)
        tags = request.POST.get('tags', '').split(',')

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.store = store
            product.save()
            product_form.save_m2m()

            for tag_name in tags:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    product.tags.add(tag)

            product.save()
            return redirect('view_store', store_name=store.name)
    else:
        product_form = ProductForm()
        user_stores = Store.objects.filter(owner=request.user)

    return render(request, 'create_product.html', {
        'product_form': product_form,
        'user_stores': user_stores,
        'authenticated': request.user.is_authenticated
    })
