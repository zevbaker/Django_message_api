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
    """
    this method returns the user token when
    the user name and password are sent in the
    body of the request.

    e.g
    {
        "username":"zevbaker",
        "password":"ab123456"
    }

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
            request (get): return all messages that match
            the user id as sender or receiver

        Returns:
            Response: Json list
        """
        messages = Message.objects.filter(
            Q(sender_id=request.user.id) | Q(receiver_id=request.user.id))
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ post new messages if you are the sender

        Args:
            request (post): message json in body

        Returns:
            Response: message if successful or error otherwise
        """
        data = request.data
        serializer = MessageSerializer(data=data)
        if serializer.is_valid() and data["sender"] == request.user.id:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, message_id):

        """find message by id where you are the sender or receiver

        Returns:
            Message | Response: message if found otherwise error
        """
        try:
            return Message.objects.get(Q(id=message_id) & (Q(sender_id=request.user.id) | Q(receiver_id=request.user.id)))
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, message_id):
        """
        get message and set the isRead field to true
        if the get request is from the receiver

        Args:
            request (get): allows access to user details
            message_id (int): id for finding the message

        Returns:
            Message | Response: message if found otherwise error
        """
        message = self.get_object(request, message_id)
        if(type(message) != Message):
            return message

        # only read if you are the receiver
        if(message.receiver_id == request.user.id):
            message.read()

        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def put(self, request, message_id):
        """
        updata message if ypu are the sender or receiver
        and the only changes is to the message contents

        Args:
            request (put): new data to update the message with
            message_id (int): id for finding the message

        Returns:
            Message | Response: message if update was successful otherwise error
        """
        message = self.get_object(request, message_id)
        if(type(message) != Message):
            return message

        data = request.data
        serializer = MessageSerializer(data=data)
        if serializer.is_valid() and message.valid_update(data):
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, message_id):
        """
        delete message if ypu are the sender or receiver

        Args:
            message_id (int): id for finding the message

        Returns:
            Response: delete successful (204) otherwise error
        """
        message = self.get_object(request, message_id)
        if(type(message) != Message):
            return message

        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        returns all messages for the current user
        and alows filtering by isRead flag in the body of the request
        by defuult returns all

        Args:
            request (get): includes access to the user id and body of the request

        Returns:
            Message | Response: messages if update was successful otherwise error
        """
        isReadFlag = None

        try:
            usersMessages = Message.objects.filter(
                Q(sender_id=request.user.id) | Q(receiver_id=request.user.id))
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if "isRead" in request.body.decode("utf-8"):
            isReadFlag = JSONParser().parse(request)["isRead"]
            if type(isReadFlag) is bool:
                usersMessages = usersMessages.filter(Q(isRead=isReadFlag))

        serializer = MessageSerializer(usersMessages, many=True)
        return Response(serializer.data)
