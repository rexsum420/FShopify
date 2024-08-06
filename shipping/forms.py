from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['customer_name', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country']
        
        