from django.urls import path
from .views import LoginView, LogoutView
from rest_registration.api.views import (send_reset_password_link,
                                         reset_password,
                                         register,
                                         verify_registration,
                                         register_email,
                                         verify_email,
                                         profile
                                         )

urlpatterns = [
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', register, name='register'),
    path('register-email/', register_email, name='register_email'),
    path('verify/email/', verify_email, name='verify_email'),
    path('verify/account/', verify_registration),
    path('reset/password/', reset_password),
    path('reset-password-link/', send_reset_password_link),
    path('profile/', profile, name='profile')
]
