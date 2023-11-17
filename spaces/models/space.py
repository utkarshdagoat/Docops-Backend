from django.db import models
from myauth.models import User
import uuid

# Create your models here.


class Space(models.Model):
    name = models.CharField(max_length=32 , unique=True)
    creater = models.ForeignKey(to=User ,related_name="workspace_creater", on_delete=models.CASCADE )
    isPrivate = models.BooleanField(default=False)
    users = models.ManyToManyField(to=User , null=True)
    invite_code = models.UUIDField(default=uuid.uuid4)
    description = models.CharField(max_length=200)

    class Meta:
        permissions = [
            ('can_create_file' , "Can Create File"),
        ]

    def get_files(self):
        from files.models.file import File
        space = Space.objects.get(id=self.id)
        return File.objects.filter(space=space)