from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="images/%Y/%m/%d/", blank=True)


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='user_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='user_to', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)


User.add_to_class("following", models.ManyToManyField('self', through=Contact, related_name="followers",
                                                      symmetrical=False))
