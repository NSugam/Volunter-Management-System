from django.core.mail import send_mail
from django.conf import settings

def generateOTP(username) :
    import math, random
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]

    subject = "Your forget password OTP"
    message = f"As you requested,\n\nYour One Time Password (OTP) is: \n\n{OTP}\n\nIf this is not requested by you. Please contact us at anonymous@admin.com"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [username]
    send_mail(subject,message,email_from,recipient_list)
    return OTP
