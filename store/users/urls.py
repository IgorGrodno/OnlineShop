from django.urls import path
from products.views import basket_remove
from users.views import login, logout, profile,registration 

app_name='products'

urlpatterns = [
    path('login/',login,name='login'),
    path('registration/',registration,name='registration'),    
    path('profile/',profile,name='profile'),
    path('logout/', logout, name='logout'),    
    path('baskets/remove/<int:basket_id>/',basket_remove,name='basket_remove')
]