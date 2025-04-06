# # accounts/urls.py

# from django.urls import path
# from . import views

# urlpatterns = [
#     path("mfa-select/", views.mfa_select, name="mfa_select"),
#     path("mfa-totp/", views.mfa_totp, name="mfa_totp"),
#     path("mfa-verify/", views.mfa_verify, name="mfa_verify"),
# ]

# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("confirm-email/", views.confirm_email, name="confirm_email"),
    path("mfa-select/", views.mfa_select, name="mfa_select"),
    path("mfa-totp/", views.mfa_totp, name="mfa_totp"),
    path("mfa-verify/", views.mfa_verify, name="mfa_verify"),
]