from django.shortcuts import render
from django.db.models import Q
from products.models import Product, Tag, Picture
from analytics.models import Analytic
from django.db.models import OuterRef, Subquery, Value, CharField
from django.db.models.functions import Concat
from datetime import timedelta
from django.utils import timezone

def index(request):
    new_threshold = timezone.now() - timedelta(days=7)
    main_image = Picture.objects.filter(product=OuterRef('pk'), main=True).values('image')[:1]
    new_products = Product.objects.all().order_by('-created_at')[:20].annotate(
        main_image=Concat(Value('https://market.s3.amazonaws.com/'), Subquery(main_image, output_field=CharField()))
    )
    
    foryou_products = None
    if request.user.is_authenticated:
        # Extract the top 20 tag names based on views in analytics
        top_tag_ids = Analytic.objects.filter(user=request.user).order_by('-views').values_list('tag', flat=True)[:20]
        top_tags = Tag.objects.filter(id__in=top_tag_ids).values_list('name', flat=True)
        
        if top_tags:
            query = Q()
            for tag in top_tags:
                query |= Q(name__icontains=tag) | Q(description__icontains=tag) | Q(category__name__icontains=tag)
            
            foryou_products = Product.objects.filter(query).distinct().order_by('-created_at')[:20].annotate(
        main_image=Concat(Value('https://market.s3.amazonaws.com/'), Subquery(main_image, output_field=CharField()))
    )
    
    return render(request, 'index.html', {
        'new_products': new_products,
        'foryou_products': foryou_products,
        'authenticated': request.user.is_authenticated,
        'new_threshold': new_threshold,
    })
