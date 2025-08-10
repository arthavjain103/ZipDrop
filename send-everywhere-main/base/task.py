from celery import shared_task
from django.utils import timezone
from .models import File
import os
import logging

logger = logging.getLogger(__name__)

@shared_task
def delete_expired_files():
    """Delete expired files from filesystem and database."""
    now = timezone.now()

    expired_files = File.objects.filter(expiration_time__lt=now)

    for file_obj in expired_files:
        try:
            
            file_path = file_obj.file.path if file_obj.file else None
            if file_path and os.path.isfile(file_path):
                os.remove(file_path)
                logger.warning(f"Deleted file from filesystem: {file_path}")

        
            file_obj.delete()
            logger.warning(f"Deleted DB record for: {file_obj.name}")

        except Exception as e:
            logger.error(f"Error deleting file {file_obj.name}: {e}")

    return f"{expired_files.count()} expired file(s) deleted"
