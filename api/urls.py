from django.urls import path
from .views import MessageListView, MessageDetailView, UserMessages, CustomAuthToken

urlpatterns = [
    path('message/', MessageListView.as_view()),
    path('message/<int:id>/', MessageDetailView.as_view()),
    path('user/<int:id>/', UserMessages.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view()),

]
