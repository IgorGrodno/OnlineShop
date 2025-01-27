
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth,messages
from django.urls import reverse

from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from products.models import Basket
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user) 
                return HttpResponseRedirect(reverse('index'))    
    context = {'form':UserLoginForm()}
    print(request.user)
    return render(request,'users/login.html',context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)  
        if form.is_valid():            
            form.save()
            messages.success(request,'Регистрация прошла успешно')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request,'users/registration.html',context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            print("POST data:", request.POST) 
            print("FILES data:", request.FILES) 
            form.save()  
            return HttpResponseRedirect(reverse('users:profile'))  
        else:
            print('Form is not valid:', form.errors)  
    else:
        form = UserProfileForm(instance=request.user)
        
        context = {
        'form': form,
        'title': 'Edit Profile',
        'baskets': Basket.objects.filter(user=request.user)        
        }
    return render(request, 'users/profile.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))