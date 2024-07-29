from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, TagForm
from .models import Tag

@login_required
def create_product(request):
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
            product.save()
            product_form.save_m2m()
            return redirect('product_list')  # Redirect to your desired page after saving
    else:
        product_form = ProductForm()
        tag_form = TagForm()
    
    return render(request, 'create_product.html', {
        'product_form': product_form,
        'tag_form': tag_form,
    })
