from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Store
from .forms import StoreForm
from .serializers import StoreSerializer
from django.urls import reverse
from products.models import Product, Picture
from django.http import HttpResponseForbidden
from django.db.models import OuterRef, Subquery, Value, CharField
from django.db.models.functions import Coalesce, Concat

@login_required(login_url='login')
def create_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            return redirect('my-stores')  # Redirect to your desired page after saving
    else:
        form = StoreForm()
    return render(request, 'create_store.html', {'form': form, 'authenticated': request.user.is_authenticated})

@login_required(login_url='login')
def my_stores(request):
    stores = Store.objects.filter(owner=request.user)
    return render(request, 'stores.html', {'stores': stores, 'authenticated': request.user.is_authenticated})

from datetime import timedelta
from django.utils import timezone

@login_required(login_url='login')
def edit_store(request, store_name):
    store = get_object_or_404(Store, name=store_name)
    if store:
        isOwner = (request.user == store.owner)
    if isOwner:
        main_image = Picture.objects.filter(product=OuterRef('pk'), main=True).values('image')[:1]
        products = Product.objects.filter(store=store).annotate(
            main_image=Concat(Value('https://market.s3.amazonaws.com/'), Subquery(main_image, output_field=CharField()))
        )
        new_threshold = timezone.now() - timedelta(days=7)
        return render(request, 'store.html', {'store': store, 'products': products, 'authenticated': request.user.is_authenticated, 'new_threshold': new_threshold})
    else:
        return HttpResponseForbidden('You are not the store owner and cannot edit this store')

    
@login_required(login_url='login')
def view_store(request, store_name):
    store = get_object_or_404(Store, name=store_name)
    main_image = Picture.objects.filter(product=OuterRef('pk'), main=True).values('image')[:1]
    products = Product.objects.filter(store=store).annotate(
            main_image=Concat(Value('https://market.s3.amazonaws.com/'), Subquery(main_image, output_field=CharField()))
        )
    new_threshold = timezone.now() - timedelta(days=7)
    return render(request, 'storefront.html', {'store': store, 'products': products, 'authenticated': request.user.is_authenticated, 'new_threshold': new_threshold})

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
