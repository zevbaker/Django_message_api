from rest_framework import serializers
from api.models import Message, UserMessages


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver',
                  'subject', 'body', 'date', 'isRead']


class UserMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessages
        fields = ['user', 'messages']
