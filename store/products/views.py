from django.shortcuts import render

from products.models import Product, ProductCategory

def index(request):
    return render(request,'products/index.html')

def products(request):
    context = {
        'title':'store - catalog',
        'products': Product.objects.all(),
        'categorys':ProductCategory.objects.all()
    }
    return render(request,'products/products.html', context)