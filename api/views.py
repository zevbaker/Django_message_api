from rest_framework.parsers import JSONParser
from .models import Message
from .serializers import MessageSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class CustomAuthToken(ObtainAuthToken):
    """[summary]

    Args:
        ObtainAuthToken ([type]): [description]
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """[summary]

        Args:
            request (get): [description]

        Returns:
            Response: Json list or
        """
        messages = Message.objects.filter(
            Q(sender_id=request.user.id) | Q(receiver_id=request.user.id))
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        """[summary]

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        data = request.data
        serializer = MessageSerializer(data=data)
        if serializer.is_valid() and len(data) > 0 and data["sender"] == request.user.id:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, message_id):
        try:
            return Message.objects.get(Q(id=message_id) & (Q(sender_id=request.user.id) | Q(receiver_id=request.user.id)))
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        message = self.get_object(request, id)
        if(type(message) != Message):
            return message

        message.read()
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def put(self, request, id):
        message = self.get_object(request, id)
        if(type(message) != Message):
            return message

        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        message = self.get_object(request, id)
        if(type(message) != Message):
            return message

        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        isReadFlag = None
        try:
            usersMessages = Message.objects.filter(
                Q(sender_id=id) | Q(receiver_id=id))
        except Message.DoesNotExist:
            return Response(status=404)

        if request.method == 'GET':
            if len(request.body) > 0 and "isRead" in request.body.decode("utf-8"):
                isReadFlag = JSONParser().parse(request)["isRead"]
            if isReadFlag is not None:
                usersMessages = usersMessages.filter(Q(isRead=isReadFlag))
            serializer = MessageSerializer(usersMessages, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)
