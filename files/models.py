from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    shared_with = models.ManyToManyField(User, related_name='shared_files', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    encrypted = models.BooleanField(default=False)  # Optional field
    file_type = models.CharField(max_length=50, blank=True, null=True)  # Add this field

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)