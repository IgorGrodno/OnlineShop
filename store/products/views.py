from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
from django.contrib import admin
from products.admin import BasketAdmin


class User(AbstractUser):
    image = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"
    
    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"Подтверждение учетной записи для {self.user.username}"
        message = (
            f"Для подтверждения адреса электронной почты для {self.user.email} "
            f"перейдите по ссылке {verification_link}"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    inlines = [BasketAdmin]


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'expiration']
    fields = ['code', 'user', 'expiration', 'created']
    readonly_fields = ['created']
