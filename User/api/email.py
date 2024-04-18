from django.core.mail import send_mail
import random
from django.conf import settings
from User.models import User



def send_otp_via_mail(email,otp):
    subject = f'Welcome to SkillBridge!! - User Verification Mail'
    otp = random.randint(1000, 9999)
    message = f'Your OTP is {otp}'
    email_from = settings.EMAIL_HOST
    try:
        send_mail(subject, message, email_from, [email])
        user_obj = User.objects.get(email=email)
        user_obj.otp = otp
        user_obj.save()
        print(f"OTP sent successfully to {email}")
        print(otp)
    except Exception as e:
        print(f"Error sending OTP to {email}: {e}")
