import uuid

from rest_framework import serializers

from spaces.models.space import Space
from spaces.models.request import Request
from myauth.models import User

from spaces.services import doesSpaceNameExist , PublicSpaceInstanceFromContext ,PivateSpaceInstanceFromContext, RequestInstanceForSendingRequest , updateRequestInstance , grantCreateFilePermission

from constants.constants import REQUEST_STATE

from myauth.serializers.serializers import UserSerializers

from files.serializers.serializer import FileSpaceShowSerializer

class PublicSpaceSerializer(serializers.ModelSerializer):
    creater = UserSerializers(read_only=True)
    isPrivate = serializers.BooleanField(default=False , read_only=True)
    invite_code = serializers.UUIDField(default=uuid.uuid4 , read_only=True)
    class Meta:
        model = Space 
        fields= ['name' , 'creater' , 'isPrivate' , 'invite_code', 'description' , 'id' ]

    def create(self, validated_data):
        return PublicSpaceInstanceFromContext(context=self.context , validated_data=validated_data)


class PrivateSpaceSerializer(serializers.ModelSerializer):
    creater = UserSerializers(read_only=True)
    users =UserSerializers(many=True , read_only=True)
    isPrivate = serializers.BooleanField(default=True , read_only=True)
    invite_code = serializers.UUIDField(default=uuid.uuid4 , read_only=True)
    class Meta:
        model=Space
        fields=[ 'name' ,'creater' , 'users' , 'invite_code' , 'isPrivate' , 'description' , 'id']

    def create(self,validated_data):
        validated_data['creater'] =  self.context['request'].user  
        validated_data['isPrivate'] = True
        grantCreateFilePermission(user=self.context['request'].user)
        instance = Space.objects.create(**validated_data)
        return instance

class SpacePermissionSerializer(serializers.Serializer):
    can_edit = serializers.BooleanField(default=False)



class SpaceUserSerializer(serializers.ModelSerializer):
    users = UserSerializers(many=True, read_only=True)
    creater = UserSerializers(read_only=True)

    class Meta:
        model = Space
        fields = ['name' , 'users', 'creater']



