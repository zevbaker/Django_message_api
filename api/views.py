from rest_framework.parsers import JSONParser
from .models import Message
from .serializers import MessageSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


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
        data = request.data
        serializer = MessageSerializer(data=data)
        if serializer.is_valid() and len(data) > 0 and data["sender"] == request.user.id:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # TODO fix try catch
    def get_object(self, request, message_id):
        try:
            return Message.objects.get(Q(id=message_id) & (Q(sender_id=request.user.id) | Q(receiver_id=request.user.id)))
        except Message.DoesNotExist:
            raise Message.DoesNotExist

    def get(self, request, id):
        try:
            message = self.get_object(request, id)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        message.read()

        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            message = self.get_object(request, id)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            message = self.get_object(request, id)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
            if isReadFlag != None:
                usersMessages = usersMessages.filter(Q(isRead=isReadFlag))
            serializer = MessageSerializer(usersMessages, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)
