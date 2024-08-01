from django.shortcuts import render
from django.db.models import Q
from products.models import Product
from analytics.models import Analytic

def index(request):
    # Get the 20 newest products
    new_products = Product.objects.all().order_by('-created_at')[:20]
    
    # Initialize an empty variable for foryou_products
    foryou_products = None
    
    # If the user is authenticated, get the 20 most relevant products
    if request.user.is_authenticated:
        # Extract the top 20 tags based on views in analytics
        top_tags = Analytic.objects.filter(user=request.user).order_by('-views').values_list('tag', flat=True)[:20]
        
        # Construct a query to find products matching the tags in name, description, or category
        foryou_products = Product.objects.filter(
            Q(name__icontains=' '.join(top_tags)) |
            Q(description__icontains=' '.join(top_tags)) |
            Q(category__name__icontains=' '.join(top_tags))
        ).distinct().order_by('-created_at')[:20]
    
    return render(request, 'index.html', {
        'new_products': new_products,
        'foryou_products': foryou_products,
        'authenticated': request.user.is_authenticated
    })
