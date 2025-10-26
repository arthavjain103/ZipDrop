from django.db import models
from django.db.models.functions import Now
from datetime import timedelta
from django.utils import timezone



def default_expiration_time():
    return timezone.now() + timedelta(minutes=5)


class FileManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            expiration_time__gt=Now()
        )


class File(models.Model):
    uuid = models.UUIDField()
    file = models.FileField(upload_to='files')
    name = models.CharField(max_length=250)
    path = models.CharField(max_length=100, null=True)
    request_code = models.CharField(max_length=6, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    expiration_time = models.DateTimeField(
        db_index=True,
        default=default_expiration_time,  
        editable=False
    )

    def is_expired(self):
        expiry_time = self.created_at + timedelta(minutes=1)
        return timezone.now() > expiry_time

  

    def __str__(self):
        return self.name


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} - {self.email}"
