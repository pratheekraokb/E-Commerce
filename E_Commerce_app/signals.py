from django.db.models.signals import post_save
from django.dispatch import receiver
from E_Commerce_app.models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_staff_superuser(sender, instance, created, **kwargs):
    if created and instance.is_staff and not instance.is_superuser:
        # Check if the user is newly created, is_staff is True, and is_superuser is not already True
        instance.is_superuser = True
        instance.save()