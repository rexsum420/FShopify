from django.shortcuts import render, get_object_or_404
from cart.cart import Cart
from shipping.models import ShippingAddress
from creditcards.models import CreditCard, BillingAddress

def checkout(request):
    if request.method == 'POST':
        return render(request, 'payment_success.html')
    else:
        cart = Cart(request)
        ship = request.GET.get('shipping')
        card = request.GET.get('card')
        bill = request.GET.get('billing')
        shipping = get_object_or_404(ShippingAddress, id=ship)
        creditcard = get_object_or_404(CreditCard, id=card)
        billing = get_object_or_404(BillingAddress, id=bill)
        return render(request, 'checkout.html', {'authenticated': request.user.is_authenticated, 'cart': cart, 'shipping': shipping, 'creditcard': creditcard, 'billing': billing})
