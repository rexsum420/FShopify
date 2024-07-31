from django import forms
from .models import Store

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'phone', 'logo', 'banner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'logo': 'Logo: <span class="label-text">(Best to use square images, e.g., 300x300)</span>',
            'banner': 'Banner: <span class="label-text">(Best to use 16:9 aspect ratio images, e.g., 1200x675)</span>',
        }
