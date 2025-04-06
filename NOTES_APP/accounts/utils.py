import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(email, code):
    sender_email = "alimzhanbaizhanov22@gmail.com"
    sender_password = "fxqkbxhuxllksulj"

    subject = "Код подтверждения"
    message = f"Ваш код подтверждения: {code}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain", "utf-8"))

    try:
        print(f"📨 Отправляем письмо на {email} с кодом: {code}")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("✅ Email отправлен!")
    except Exception as e:
        print(f"Ошибка при отправке Email: {e}")
