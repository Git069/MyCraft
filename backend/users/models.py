from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    Extends the default User model to include additional user information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_craftsman = models.BooleanField(default=False, verbose_name="Is Craftsman")
    # You can add more fields here later, e.g., phone_number, profile_picture, etc.

    def __str__(self):
        return f"{self.user.username}'s Profile"

# --- Signal Handler ---
# This function is triggered whenever a User object is saved.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile for a new user, or updates the existing one.
    """
    if created:
        Profile.objects.create(user=instance)
    # We use a try/except block here because in some rare cases (like during initial migration),
    # the profile might not exist yet when save is called.
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
