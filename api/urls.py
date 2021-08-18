from django.urls import path
from .views import MessageListView, MessageDetailView, UserMessages
from rest_framework.authtoken.views import ObtainAuthToken
from .views import redirect_view

urlpatterns = [
    path('message/', MessageListView.as_view()),
    path('message/<int:id>/', MessageDetailView.as_view()),
    path('user/<int:id>/', UserMessages.as_view()),
    path('api-token-auth/', ObtainAuthToken, name='api_token_auth'),
    path('accounts/profile/', redirect_view),

]
