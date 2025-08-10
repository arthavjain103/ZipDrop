import time
from . import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import random
import math
from .models import Feedback
from django.core.mail import send_mail
from django.conf import settings 


def generateCode():
    digits = [i for i in range(0, 10)]
    random_str = ""

    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str


@receiver(post_save, sender=models.File)
def createRequestCode(sender, instance, created, **kwargs):
    if created:
        instance.request_code = generateCode()
        instance.save()
        print("Request code created")
        
@receiver(post_save , sender = Feedback)
def send_feedback_email(sender, instance, created, **kwargs):
    if created:
        print(f"Signal Triggered: Sending email for {instance.email}")
        try:
            send_mail(
                f"New Feedback from {instance.name}",
                f"Message: {instance.message}\nFrom: {instance.email}",
                settings.DEFAULT_FROM_EMAIL,
                ["arthavjain105@gmail.com"],
                fail_silently=False,
            )
            print(" Email sent successfully!")
        except Exception as e:
            print(" Email send failed:", e)