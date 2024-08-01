from django.shortcuts import render
from cart.cart import Cart

def checkout(request):
    cart = Cart(request)
    return render(request, 'checkout.html', {'authenticated': request.user.is_authenticated, 'cart': cart})