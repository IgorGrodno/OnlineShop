import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import EmailVerification
from django.utils.crypto import get_random_string

User = get_user_model()


@pytest.mark.django_db
def test_user_login_view(client, user):
    url = reverse('users:login')
    response = client.get(url)
    assert response.status_code == 200
    assert 'users/login.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_user_registration_view(client):
    url = reverse('users:registration')
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'Testpassword123!',
        'password2': 'Testpassword123!',
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after success
    assert User.objects.filter(username='testuser').exists()


@pytest.mark.django_db
def test_user_profile_view(client, user):
    client.force_login(user)
    url = reverse('users:profile', args=[user.id])
    response = client.get(url)
    assert response.status_code == 200
    assert 'users/profile.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_logout_view(client, user):
    client.force_login(user)
    url = reverse('users:logout')
    response = client.get(url)
    assert response.status_code == 302  # Redirect to index
    assert response.url == reverse('index')
    

@pytest.mark.django_db
def test_email_verification_view(client, user):
    code = get_random_string(32)
    EmailVerification.objects.create(user=user, code=code)
    url = reverse('users:email_verification', 
                  kwargs={'email': user.email, 'code': code})
    response = client.get(url)
    user.refresh_from_db()
    assert response.status_code == 200
    assert user.is_verified_email
