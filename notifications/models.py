from django.db import models

from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


from myauth.models import User

# Create your models here.



class NotificationsChoice(models.IntegerChoices):    
    REQUEST_TO_JOIN_SPACE = 0, _('Request to join space')

CHOICES = [
    (0, _('Request to join space')),
    (1, _('Request to edit a file'))
]


class Notification(models.Model):
    message = models.CharField(max_length=100)
    recipent = models.ForeignKey(to=User , on_delete=models.CASCADE)
    notif_type = models.IntegerField(choices=CHOICES)
    unread = models.BooleanField(default=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType , on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type' , 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=['content_type' , 'object_id'])
        ]