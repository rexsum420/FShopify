from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Review, Rating
from products.models import Product
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def create_rating(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        product_id = request.POST.get('product_id')
        
        if rating and product_id:
            rating_value = int(rating)
            product = get_object_or_404(Product, id=product_id)
            
            if 0 < rating_value < 6:
                try:
                    Rating.objects.create(product=product, rating=rating_value, user=request.user)
                    url = reverse('product-detail') + f'?product_id={product_id}'
                    return HttpResponseRedirect(url)
                except:
                    url = reverse('product-detail') + f'?product_id={product_id}'
                    return HttpResponseRedirect(url)
            return render(request, 'invalid_rating.html', {'authenticated': request.user.is_authenticated})
    
    elif request.method == 'GET':
        rating = request.GET.get('rating')
        product_id = request.GET.get('product_id')
        
        if rating and product_id:
            rating_value = int(rating)
            product = get_object_or_404(Product, id=product_id)
            
            if 0 < rating_value < 6:
                try:
                    Rating.objects.create(product=product, rating=rating_value, user=request.user)
                    url = reverse('product-detail') + f'?product_id={product_id}'
                    return HttpResponseRedirect(url)
                except:
                    url = reverse('product-detail') + f'?product_id={product_id}'
                    return HttpResponseRedirect(url)
            else:
                return render(request, 'invalid_rating.html', {'authenticated': request.user.is_authenticated})
    
    return redirect('home')

@login_required(login_url='login')
def create_review(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        product_id = request.POST.get('product')
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        Review.objects.create(user=user, product=product, comment=comment)
        url = reverse('product-detail') + f'?product_id={product_id}'
        return HttpResponseRedirect(url)
        