from django.http import StreamingHttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from .services import listen_to_channel, is_user_recipient
from .render import ServerSentEventRenderer

from .serializers import NotificationSerializer

from docops.authentication import CsrfExemptSessionAuthentication

from .models import Notification

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
   
    def get_queryset(self):
        return  Notification.objects.filter(unread=True , recipent=self.request.user)



class NotificationDeleteAPIView(generics.DestroyAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication]





