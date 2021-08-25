from django.contrib import admin
from .models import Message, UserMessages

admin.site.register(Message)
admin.site.register(UserMessages)
