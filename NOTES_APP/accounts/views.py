# # accounts/views.py

# import pyotp, qrcode, io, base64, time
# from django.core.mail import send_mail
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.conf import settings
# from django.contrib import messages

# def bbs_random(seed, p=499, q=547):
#     n = p * q
#     seed = (seed ** 2) % n
#     return seed % 900000 + 100000

# @login_required
# def mfa_select(request):
#     if request.method == "POST":
#         method = request.POST.get("mfa_method")
#         request.session["mfa_method"] = method

#         if method == "email":
#             seed = int(time.time())
#             code = str(bbs_random(seed))
#             request.session["mfa_code"] = code

#             send_mail(
#                 "Код MFA",
#                 f"Ваш код подтверждения: {code}",
#                 settings.DEFAULT_FROM_EMAIL,
#                 [request.user.email],
#             )
#             return redirect("mfa_verify")

#         elif method == "totp":
#             return redirect("mfa_totp")

#     return render(request, "accounts/mfa_select.html")

# @login_required
# def mfa_totp(request):
#     secret = request.user.profile.totp_secret
#     totp = pyotp.TOTP(secret)
#     uri = totp.provisioning_uri(name=request.user.username, issuer_name="DjangoNotes")

#     img = qrcode.make(uri)
#     buffer = io.BytesIO()
#     img.save(buffer, format='PNG')
#     qr_b64 = base64.b64encode(buffer.getvalue()).decode()

#     return render(request, "accounts/mfa_totp.html", {"qr": qr_b64})

# @login_required
# def mfa_verify(request):
#     if request.method == "POST":
#         code = request.POST.get("code")
#         method = request.session.get("mfa_method")

#         if method == "email" and code == request.session.get("mfa_code"):
#             request.session["mfa_passed"] = True
#             return redirect("dashboard")

#         elif method == "totp":
#             totp = pyotp.TOTP(request.user.profile.totp_secret)
#             if totp.verify(code):
#                 request.session["mfa_passed"] = True
#                 return redirect("dashboard")

#         messages.error(request, "Неверный код!")

#     return render(request, "accounts/mfa_verify.html")



# accounts/views.py

import pyotp
import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Profile
from django.contrib.auth.decorators import login_required
import time

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Имя пользователя уже занято.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Эта почта уже зарегистрирована.")
            return redirect("register")

        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, "Этот номер уже используется.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Генерация TOTP секрета
        totp_secret = pyotp.random_base32()
        user.profile.totp_secret = totp_secret
        user.profile.phone = phone
        user.profile.save()

        # Сохраняем код подтверждения в сессии
        code = random.randint(100000, 999999)
        request.session["email_code"] = code
        request.session["registered_user_id"] = user.id

        # Отправляем код на email
        send_mail(
            subject="Подтверждение почты",
            message=f"Ваш код подтверждения: {code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect("confirm_email")

    return render(request, "accounts/register.html")

def confirm_email(request):
    if request.method == "POST":
        input_code = request.POST.get("code")
        if int(input_code) == int(request.session.get("email_code", 0)):
            user_id = request.session.get("registered_user_id")
            user = User.objects.get(id=user_id)
            user.profile.email_confirmed = True
            user.profile.save()

            # Чистим сессию
            del request.session["email_code"]
            del request.session["registered_user_id"]

            messages.success(request, "Email подтверждён. Можете войти.")
            return redirect("login")
        else:
            messages.error(request, "Неверный код.")

    return render(request, "accounts/confirm_email.html")

def bbs_random(seed, p=499, q=547):
    n = p * q
    seed = (seed ** 2) % n
    return seed % 900000 + 100000  # 6-значный код

@login_required
def mfa_select(request):
    if request.method == "POST":
        method = request.POST.get("mfa_method")
        request.session["mfa_method"] = method

        if method == "email":
            seed = int(time.time())
            code = str(bbs_random(seed))
            request.session["mfa_code"] = code
            user_email = request.user.email

            send_mail(
                subject="Код MFA",
                message=f"Ваш код подтверждения: {code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
            )
            return redirect("mfa_verify")

        elif method == "totp":
            return redirect("mfa_totp")

    return render(request, "accounts/mfa_select.html")

@login_required
def mfa_totp(request):
    import pyotp
    import qrcode
    import io
    import base64

    secret = request.user.profile.totp_secret
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=request.user.username, issuer_name="DjangoNotesApp")

    # Создаём QR-код
    img = qrcode.make(uri)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "accounts/mfa_totp.html", {"qr": qr_b64})


@login_required
def mfa_verify(request):
    if request.method == "POST":
        code = request.POST.get("code")
        method = request.session.get("mfa_method")

        if method == "email":
            if code == request.session.get("mfa_code"):
                request.session["mfa_passed"] = True
                return redirect("dashboard")  # или любую защищённую страницу
            else:
                messages.error(request, "Неверный код")

        elif method == "totp":
            import pyotp
            secret = request.user.profile.totp_secret
            totp = pyotp.TOTP(secret)
            if totp.verify(code):
                request.session["mfa_passed"] = True
                return redirect("dashboard")
            else:
                messages.error(request, "Неверный TOTP код")

    return render(request, "accounts/mfa_verify.html")
