
from django.shortcuts import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from common.views import TitleMixin
from users.models import User, EmailVerification
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegistrationView(SuccessMessageMixin, TitleMixin,  CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Регистрация прошла успешно'
    title = 'Регистрация'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile',args=(self.object.id,))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Подтвнрждение EMail'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(
            user=user, code=code)
        if email_verifications.exists():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(
                request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
