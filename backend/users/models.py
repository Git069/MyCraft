"""Models for the Users application.

This module defines the Profile model which extends the built-in User model
to include additional information such as craftsman status, address details,
and profile pictures.
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def profile_picture_path(instance, filename):
    """Generate the file path for a user's profile picture.

    Args:
        instance: The Profile instance.
        filename: The original filename of the uploaded image.

    Returns:
        str: The path where the file will be saved, in the format:
             'profile_pics/user_<id>/<filename>'
    """
    # file will be uploaded to MEDIA_ROOT/profile_pics/user_<id>/<filename>
    return f'profile_pics/user_{instance.user.id}/{filename}'


class Profile(models.Model):
    """User Profile model extending the default Django User.

    Stores additional information about the user, including craftsman-specific
    details and a profile picture.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_craftsman = models.BooleanField(default=False, verbose_name="Is Craftsman")

    # --- Craftsman fields ---
    company_name = models.CharField(max_length=255, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # --- New Profile Picture field ---
    profile_picture = models.ImageField(upload_to=profile_picture_path, null=True, blank=True)

    def __str__(self):
        """Return a string representation of the profile.

        Returns:
            str: The username followed by "'s Profile".
        """
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Signal receiver to create or update the user profile.

    Automatically creates a Profile instance when a new User is created,
    and saves the Profile when the User is saved.

    Args:
        sender: The model class (User).
        instance: The actual instance being saved.
        created: Boolean; True if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        Profile.objects.create(user=instance)
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
