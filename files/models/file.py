import uuid
import os

from django.db import models
from myauth.models import User
from spaces.models.space import Space


def get_filename(instance , filename):
    stringId = str(uuid.uuid4())
    extension = os.path.splitext(filename)[1]
    filename_reformat = stringId + '/'+instance.space.name + extension
    return filename_reformat




class File(models.Model):
    createdBy =models.ForeignKey(to=User , on_delete=models.CASCADE)
    isPrivate = models.BooleanField(default=False)
    inviteCode = models.UUIDField(default=uuid.uuid4 , unique=True)
    users = models.ManyToManyField(to=User , related_name="allowed_user_for_file")
    space = models.ForeignKey(to=Space , on_delete=models.CASCADE)
    docId = models.CharField(max_length=24 , null=True , blank=True , unique=True)
    heading  = models.CharField(max_length=64 , blank=True , null=True)
    cover = models.ImageField(upload_to=get_filename , null=True , blank=True)

    class Meta:
        permissions = [
           ('can_comment' , 'Can comment'),
           ('can_edit' , 'Can Edit')
        ]

    @property
    def text(self):
        file = File.objects.get(id=self.id)
        file_text = FileText.objects.get(file=file)
        return file_text.text


class FileText(models.Model):
    file = models.OneToOneField(to=File , on_delete=models.CASCADE)
    text = models.TextField(blank=True)