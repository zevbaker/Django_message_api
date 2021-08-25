from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status



@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Message_sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Message_receiver')
    subject = models.CharField(max_length=256)
    body = models.CharField(max_length=2048)
    date = models.DateTimeField(auto_now_add=True)
    isRead = models.BooleanField(name='isRead', default=False)

    fields = ['sender', 'receiver', 'subject', 'body', 'date', 'isRead']

    def read(self):
        self.isRead = True
        self.save()

    def valid_update(self, newMessage):
        if(self.sender_id == newMessage["sender"] and self.receiver_id == newMessage["receiver"]):
            self.body = newMessage["body"]
            self.subject = newMessage["subject"]
            self.save()
            return True
        return False

    def delete(self, user):
        test = UserMessages.objects.get(user=user).messages.remove(self)
        print(test)

    def __str__(self):
        return f'{self.date} {self.sender} -> {self.receiver} :subject : {self.subject}, body : {self.body}'


class UserMessages(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    messages = models.ManyToManyField(Message)

    fields = ['user', 'messages']

    @receiver(post_save, sender=Message)
    def add_new_message(sender, instance=None, created=False, **kwargs):
        if created:
            # # print(sender.Message_sender)
            # # field_sender = 'sender'
            # # field_receiver = 'receiver'
            # # obj = Message.objects.first()
            # # field_sender = Message._meta.get_field(field_sender)
            # # field_receiver = Message._meta.get_field(field_receiver)
            # # field_value_sender = field_sender.value_from_object(obj)
            # # field_value_receiver = field_receiver.value_from_object(obj)

            senders_messages = UserMessages.objects.get(user=User.objects.get(id=instance.sender_id))
            receiver_messages = UserMessages.objects.get(user=User.objects.get(id=instance.receiver_id))

            senders_messages.messages.add(instance)
            receiver_messages.messages.add(instance)


    def get_user_messages(user_id):
        return UserMessages.objects.get(user=User.objects.get(id=user_id)).messages

    def get_one_message_or_404(user_id,message_id):
        try:
            return UserMessages.get_user_messages(user_id).get(Q(id=message_id) & (Q(sender_id=user_id) | Q(receiver_id=user_id)))
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def __str__(self):
        return f'{self.user} messages'

