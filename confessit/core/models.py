from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
class Tag(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    parent_comment = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    is_approved = models.BooleanField(default=True)

class Confession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=30)
    description = models.TextField()
    tags = models.ManyToManyField('Tag',null=False)
    created_at = models.DateTimeField(auto_created=True,auto_now_add=True)
    comments = models.ManyToManyField('Comment', blank=True)
    is_approved = models.BooleanField(default=False)
    favourites = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='favourite_confessions')

    def get_absolute_url(self):
        return reverse('confession_detail', kwargs={'pk': self.pk})


    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')
    avatar = models.ImageField(default='avatars/default_avatar.png',
        upload_to='avatars/',
        verbose_name="Аватар")

class Comment_tba(models.Model):
    comment = models.ForeignKey('Comment',on_delete=models.CASCADE)
class Confession_tba(models.Model):
    confession = models.ForeignKey('Confession',on_delete=models.CASCADE)
