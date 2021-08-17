from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None,created=False ,**kwargs):
    if created:
        Token.objects.create(user=instance)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Message_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Message_receiver')
    subject = models.CharField(max_length=200)
    body = models.CharField(max_length=2000)
    date = models.DateTimeField(auto_now_add=True)
    isRead = models.BooleanField(name='isRead', default=False)

    fields = ['sender', 'receiver', 'subject', 'body','date','isRead']

    def __str__(self):
        return f'{self.date} {self.sender} -> {self.receiver} : subject : {self.subject}, body : {self.body}' 