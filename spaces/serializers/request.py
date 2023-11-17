from spaces.models.request import Request
from constants.constants import REQUEST_STATE

from rest_framework import serializers

from spaces.services import RequestInstanceForSendingRequest , updateRequestInstance 
from myauth.serializers.serializers import UserSerializers
from .space import PublicSpaceSerializer

class RequestSerializer(serializers.ModelSerializer):
    space = serializers.PrimaryKeyRelatedField(read_only=True)
    from_user = UserSerializers(read_only=True)
    state = serializers.ChoiceField(choices=REQUEST_STATE , default=REQUEST_STATE[0] , read_only=True)
    invite_code = serializers.CharField(max_length=56)
    creator = UserSerializers(read_only=True)


    class Meta:
        model = Request
        fields = ['space' , 'from_user' , 'state' , 'invite_code' , 'creator']

    def create(self,validated_data):
        return RequestInstanceForSendingRequest(context=self.context , validated_data=validated_data)


class RequestNotificationSerializer(serializers.ModelSerializer):
    from_user = UserSerializers(read_only=True)
    creator = UserSerializers(read_only=True)
    
    class Meta:
        model = Request
        fields = ['from_user' , 'state' , 'creator' , 'id']

class RequestStateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Request
        fields = ['state']


class AcceptOrRejectRequestSerializer(serializers.ModelSerializer):

    state = serializers.ChoiceField(choices=[REQUEST_STATE[1] , REQUEST_STATE[2]])
    permission = serializers.BooleanField(default=False)
    
    class Meta:
        model = Request
        fields = ['state' , 'permission']
    
    def update(self, instance, validated_data):
        return  updateRequestInstance(context=self.context , instance=instance , validated_data=validated_data)
        