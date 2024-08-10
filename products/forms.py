from django import forms
from .models import Product, Picture
from ckeditor.widgets import CKEditorWidget

class ProductForm(forms.ModelForm):
    quantity = forms.IntegerField(label='Stock Quantity', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    low_stock_threshold = forms.IntegerField(label='Low Stock Threshold', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        exclude = ['tags', 'store']
        fields = [
            'name', 'description', 'price', 'category', 'quantity', 'low_stock_threshold',
            'size', 'color', 'brand', 'model_number', 'weight'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': CKEditorWidget(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['image', 'alt', 'main']
