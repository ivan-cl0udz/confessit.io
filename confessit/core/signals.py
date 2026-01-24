from django.db.models.signals import post_save,pre_save
from .models import Comment,Confession,Profile,Tag
from django.dispatch import receiver
from django.conf import settings
import logging
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Confession_tba,Comment_tba

@receiver(post_save,sender=Confession)
def email_to_approve(instance,**kwargs):
    send_mail(subject=f'New confession was made and requires checking',
              message=f'There was a new confession made, details(id:{instance.id},title:{instance.title})',
              from_email= settings.EMAIL_HOST_USER,
              recipient_list=['ivanfilipets115@gmail.com'])
    

@receiver(post_save,sender=Comment)
def email_to_approve_comment(instance,**kwargs):
    send_mail(subject=f'New comment was made and requires checking',
              message=f'There was a new comment made, details(user:{instance.user},id:{instance.id})',
              from_email= settings.EMAIL_HOST_USER,
              recipient_list=['ivanfilipets115@gmail.com'])
@receiver(post_save,sender=User)
def create_profile(instance,created,**kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
@receiver(post_save,sender=Tag)
def email_to_approve_tag(instance,**kwargs):
    send_mail(subject=f'New tag was created by user and requires checking',
              message=f'There was a new tag made, details(name:{instance.name})',
              from_email= settings.EMAIL_HOST_USER,
              recipient_list=['ivanfilipets115@gmail.com'])