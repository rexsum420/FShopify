from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, TagForm
from .models import Tag, Product
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import ProductSerializer
from store.models import Store

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(store=self.request.user.store)

@login_required
def create_product(request):
    store_name = request.GET.get('store_name')
    if not store_name:
        return redirect('product_list')  # Redirect if no store_name is provided

    store = get_object_or_404(Store, name=store_name)
    if store.owner != request.user:
        return HttpResponseForbidden("You do not own this store.")

    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        tag_form = TagForm(request.POST)
        
        if 'add_tag' in request.POST and tag_form.is_valid():
            tag_name = tag_form.cleaned_data['name']
            tag, created = Tag.objects.get_or_create(name=tag_name)
            request.POST = request.POST.copy()
            request.POST.setlist('tags', list(set(request.POST.getlist('tags') + [str(tag.id)])))
        
        if 'create_product' in request.POST and product_form.is_valid():
            product = product_form.save(commit=False)
            product.store = store
            product.save()
            product_form.save_m2m()
            return redirect('product_list')  # Redirect to your desired page after saving
    else:
        product_form = ProductForm()
        tag_form = TagForm()
    
    return render(request, 'create_product.html', {
        'product_form': product_form,
        'tag_form': tag_form,
        'store_name': store_name,
    })