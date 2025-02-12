from django.urls import path

from orders.views import (
    OrderCreateView, 
    CanceledTempalateView, 
    OrderDetailView, 
    OrderListView, 
    SuccesTemplateView
)


app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccesTemplateView.as_view(), name='order_success'),
    path(
        'order-canceled/', 
        CanceledTempalateView.as_view(), 
        name='order_canceled'
    ),
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    ]
