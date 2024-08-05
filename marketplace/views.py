from django.shortcuts import render
from django.db.models import Q, OuterRef, Subquery, Value, CharField
from django.db.models.functions import Concat
from products.models import Product, Tag, Picture
from analytics.models import Analytic
from datetime import timedelta
from django.utils import timezone

def get_main_image_annotation():
    return Concat(Value('https://market.s3.amazonaws.com/'), Subquery(
        Picture.objects.filter(product=OuterRef('pk'), main=True).values('image')[:1],
        output_field=CharField()
    ))

def index(request):
    new_threshold = timezone.now() - timedelta(days=7)

    new_products = Product.objects.all().order_by('-created_at')[:20].annotate(
        main_image=get_main_image_annotation()
    )
    hot_products = Product.objects.all().order_by('-views')[:20].annotate(
        main_image=get_main_image_annotation()
    )
    
    foryou_products = None
    if request.user.is_authenticated:
        top_tag_ids = Analytic.objects.filter(user=request.user).order_by('-views').values_list('tag', flat=True)[:20]
        top_tags = Tag.objects.filter(id__in=top_tag_ids).values_list('name', flat=True)
        
        if top_tags:
            query = Q()
            for tag in top_tags:
                query |= Q(name__icontains=tag) | Q(description__icontains=tag) | Q(category__name__icontains=tag)
            
            foryou_products = Product.objects.filter(query).distinct().order_by('-created_at')[:20].annotate(
                main_image=get_main_image_annotation()
            )
    
    return render(request, 'index.html', {
        'new_products': new_products,
        'foryou_products': foryou_products,
        'hot_products': hot_products,
        'authenticated': request.user.is_authenticated,
        'new_threshold': new_threshold,
    })
