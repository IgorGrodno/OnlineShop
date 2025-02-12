from django.contrib import admin
from products.models import Product, ProductCategory, Basket
admin.site.register(ProductCategory)
admin.site.register(Basket)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'category']
    fields = [
        'name', 'description', 'price', 'quantity', 
        'image', 'stripe_product_price_id', 'category'
    ]
    search_fields = ['name']
    ordering = ['-name']


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ['product', 'quantity']
    extra = 0
