from django.urls import include, path
from .views import MessageListView,MessageDetailView,UserMessages


urlpatterns = [
    path('message/', MessageListView.as_view()),
    path('message/<int:id>/', MessageDetailView.as_view()),
    path('user/<int:id>/', UserMessages.as_view()),
    path('api-auth/', include('rest_framework.urls')),

]
