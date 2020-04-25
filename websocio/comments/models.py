from django.db import models

# Create your models here.


class Comment(models.Model):
    created = models.DateField(auto_now_add=True, db_index=True)
    image = models.ForeignKey('images.image', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()

    class Meta:
        ordering = ('-created',)