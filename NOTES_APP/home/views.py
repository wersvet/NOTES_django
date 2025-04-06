import random
import string
import uuid

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.urls import reverse
from .models import EmailVerification, TwoFactorCode
from django.conf import settings
from django.contrib.auth import login 
from django.contrib.auth.models import User



class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if user.is_superuser:
            login(self.request, user)
            return redirect('notes.list')
        code = ''.join(random.choices(string.digits, k=6))
        TwoFactorCode.objects.create(user=user, code=code)
        send_2fa_email(user, code)
        self.request.session['2fa_user_id'] = user.id
        return redirect('verify_2fa')

def send_2fa_email(user, code):
    subject = 'Ваш код 2FA'
    message = f'Ваш код для входа: {code}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        request.session.flush()  # Полностью очищаем сессию
        return response

class HomeView(TemplateView):
    template_name = 'home/welcome_site.html'


class SighupView(CreateView):
    form_class = CustomUserCreationForm 
    template_name = 'home/register.html'
    success_url = '/smart/notes'

    def form_valid(self, form):
        user = form.save()
        send_verification_email(self.request, user)  # Отправляем письмо
        return HttpResponse("Проверьте почту для подтверждения.")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes.list')
        return super().get(request, *args, **kwargs)

def send_verification_email(request, user):
    verification = EmailVerification.objects.create(user=user)
    verification_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'code': str(verification.code)})
    )
    subject = 'Подтверждение регистрации'
    message = f'Перейдите по ссылке для подтверждения: {verification_url}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])



class VerifyEmailView(View):
    def get(self, request, code):
        try:
            verification = EmailVerification.objects.get(code=code)
            user = verification.user
            user.is_active = True
            user.save()
            verification.delete()
            return redirect('login')
        except EmailVerification.DoesNotExist:
            return HttpResponse("Неверный код подтверждения.")
        


class Verify2FAView(View):
    template_name = 'home/verify_2fa.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        code = request.POST.get('code')
        user_id = request.session.get('2fa_user_id')
        if not user_id:
            return redirect('login')
        try:
            user = User.objects.get(id=user_id) 
            two_factor = TwoFactorCode.objects.filter(user=user, code=code).latest('created_at')
            two_factor.delete()
            login(request, user)  # Авторизуем пользователя
            del request.session['2fa_user_id']  # Удаляем временные данные из сессии
            return redirect('notes.list')
        except (TwoFactorCode.DoesNotExist, User.DoesNotExist):
            return HttpResponse("Неверный код.")