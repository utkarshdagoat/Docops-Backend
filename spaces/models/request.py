from django.db import models

from .space import Space
from myauth.models import User
from constants.constants import REQUEST_STATE

from django.contrib.contenttypes.fields import GenericRelation

from notifications.models import Notification

class Request(models.Model):
    space = models.ForeignKey(to=Space , on_delete=models.CASCADE)
    from_user = models.ForeignKey(to=User , on_delete=models.CASCADE)
    state = models.CharField(choices=REQUEST_STATE)
    notif = GenericRelation(to=Notification)

    @property
    def invite_code(self):
        return self.space.invite_code 
    
    @property
    def permission(self):
        return self.from_user.has_perm("spaces.can_edit_file")
    
    @property
    def creator(self):
        space = Space.objects.get(id=self.space.id)
        return space.creater

    class Meta:
        verbose_name = "Request"