from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ShippingForm
from .models import ShippingAddress

@login_required(login_url='login')
def create_shipping(request):
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = request.user
            shipping.save()
            return redirect('select-shipping')
    else:
        form = ShippingForm()
    return render(request, 'add_shipping.html', {'form': form})

@login_required(login_url='login')
def select_shipping(request):
    shippings = ShippingAddress.objects.filter(user=request.user)
    return render(request, 'select_shipping.html', {'shippings': shippings})