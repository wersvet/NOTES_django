from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),

    path('login/',views.LoginInterfaceView.as_view(),name='login'),
    path('logout/',views.LogoutInterfaceView.as_view(),name='logout'),
    path('signup/',views.SighupView.as_view(),name='signup'),
    path('verify/<uuid:code>/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('verify-2fa/', views.Verify2FAView.as_view(), name='verify_2fa'),
]