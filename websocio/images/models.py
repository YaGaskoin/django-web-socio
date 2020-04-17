from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.


class Image(models.Model):
    url = models.URLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_image", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="images_liked", blank=True)
    total_likes = models.PositiveIntegerField(blank=True, default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)