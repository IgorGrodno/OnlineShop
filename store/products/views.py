from django.http import HttpResponseRedirect
from django.shortcuts import render

from products.models import Product, ProductCategory, Basket
from users.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'products/index.html')

def products(request):
    context = {
        'title':'store - catalog',
        'products': Product.objects.all(),
        'categorys':ProductCategory.objects.all()
    }
    return render(request,'products/products.html', context)

@login_required
def basket_add(request, product_id):
    print(product_id)
    product=Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product,quantity=1)
    else:
        basket=baskets.first()
        basket.quantity+=1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])