from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreditCardForm, CreditCardFormSet
from .models import CreditCard

@login_required(login_url='login')
def add_credit_card(request):
    if request.method == "POST":
        card_form = CreditCardForm(request.POST)
        formset = CreditCardFormSet(request.POST)
        if card_form.is_valid() and formset.is_valid():
            credit_card = card_form.save(commit=False)
            credit_card.user = request.user
            credit_card.save()
            
            # Save the formset with the credit card instance
            formset.instance = credit_card
            formset.save()
            
            return redirect('select-payment')  # Replace with your success URL
    else:
        card_form = CreditCardForm()
        formset = CreditCardFormSet()
    
    return render(request, 'add_credit_card.html', {'card_form': card_form, 'formset': formset})

@login_required(login_url='login')
def select_payment(request):
    shipping = request.GET.get('shipping')
    cards = CreditCard.objects.filter(user=request.user).prefetch_related('billingaddress')
    return render(request, 'select_payment.html', {'cards': cards, 'shipping': shipping})