from rest_framework import serializers

from spaces.models import Space

from files.serializers.serializer import FileSpaceShowSerializer
from .serializers import UserSerializers

class UserSpacesSerializers(serializers.ModelSerializer):
    users = UserSerializers(many=True , read_only=True)
    files = FileSpaceShowSerializer(source='get_files' , many=True)
    class Meta:
        model = Space
        fields = ['name' , 'description', 'users' , 'isPrivate' , 'creater' ,'invite_code'  , 'files']