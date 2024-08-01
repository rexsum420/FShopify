from django.shortcuts import render
from products.models import Product
from django.db.models import F, Value
from django.db.models.functions import Concat

def search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.annotate(
        relevance=Concat(
            F('name'), 
            Value(' '), 
            F('description'), 
            Value(' '), 
            F('category__name')
        )
    ).filter(relevance__icontains=query).order_by('-relevance')

    return render(request, 'search_results.html', {'products': products, 'authenticated': request.user.is_authenticated})
