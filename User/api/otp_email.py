from django.core.mail import send_mail
from django.conf import settings
from User.models import User

import random

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])

def send_otp(email, otp):
    subject = f'Welcome to SkillBridge!! - User Verification Mail'
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



from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.core.mail import send_mail

def send_password_reset_email(user, reset_link):
    subject = 'Password Reset Request'
    message = f"Hello {user.username},\n\n"
    message += f"We received a request to reset your password. If you didn't make this request, please ignore this email.\n\n"
    message += f"To reset your password, click on the following link:\n{reset_link}\n\n"
    message += "This link will expire in 24 hours.\n\n"
    message += "If you have any issues, please contact support.\n\n"
    message += "Thanks!\nYour Application Team"
    
    send_mail(subject, message, 'from@SkillBridge.com', [user.email], fail_silently=False)




import hashlib
def generate_hash(user_id):
    secret_key = 'xAbhINandYsKilLLeaRNz'
    data = f"{user_id}-{secret_key}"
    
    hash_value = hashlib.sha256(data.encode()).hexdigest()
    return hash_value
