from django.urls import path
from users.views import UserProfileView, UserLoginView, logout,  UserRegistrationView, EmailVerificationView 
from django.contrib.auth.decorators import login_required
app_name='products'

urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('registration/',UserRegistrationView.as_view(),name='registration'),    
    path('profile/<int:pk>',login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<uuid:code>/',EmailVerificationView.as_view(),name='email_verification')
    ]