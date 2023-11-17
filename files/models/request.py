from django.db import models
from myauth.models import User
from .file import File

class RequestStatus(models.IntegerChoices):
    REJECTED = (0 , 'Rejected')
    ACCEPTED = (1, 'Accepted')

class Request(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(to=User , on_delete=models.CASCADE , related_name='user_requested_file_access')
    file = models.ForeignKey(to=File , on_delete=models.CASCADE , to_field='docId' )
    state = models.IntegerField(choices=RequestStatus.choices , default=RequestStatus.REJECTED)

    @property
    def docId(self):
        return self.file.docId
