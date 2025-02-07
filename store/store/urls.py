
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from products.views import IndexView
from orders.views import stripe_webhook_view
from rest_framework.routers import DefaultRouter
from API.viewsets import (
    BasketViewSet,
    OrderViewSet,
    UserViewSet,
    ProductViewSet,
    ProductCategoryViewSet
)

router = DefaultRouter()
router.register(r'order', OrderViewSet)
router.register(r'user', UserViewSet)
router.register(r'product', ProductViewSet)
router.register(r'basket', BasketViewSet)
router.register(r'productcategory', ProductCategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
    path('accounts/', include('allauth.urls')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('webhook/stripe/', stripe_webhook_view, name='stripe_webhook'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
