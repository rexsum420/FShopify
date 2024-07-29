from django import forms
from .models import Product, Category
from inventory.models import Inventory

class ProductForm(forms.ModelForm):
    quantity = forms.IntegerField(label='Stock Quantity', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    low_stock_threshold = forms.IntegerField(label='Low Stock Threshold', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        exclude = ['tags', 'store']
        fields = ['name', 'description', 'price', 'category', 'quantity', 'low_stock_threshold']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
