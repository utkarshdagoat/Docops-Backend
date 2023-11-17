from rest_framework import serializers
from files.models.request import Request 
from  myauth.serializers.serializers import UserSerializers

from files.models.file import File

from spaces.tasks import send_notification_request

from typing import Any

from guardian.shortcuts import assign_perm

class RequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializers(read_only=True)
    file = serializers.PrimaryKeyRelatedField(read_only=True)
    docId = serializers.CharField(required=True)
    class Meta:
        model = Request
        fields = ['docId' , 'from_user' , 'id' , 'created_at' , 'state' , 'file']

    

    def create(self , validated_data:dict[str , Any]):
        validated_data['from_user'] = self.context['request'].user
        validated_data['file'] = File.objects.get(docId=validated_data['docId'])
        validated_data['state'] = 0
        instance = Request.objects.create(
            from_user=validated_data['from_user'],
            file=validated_data['file'],
            state=validated_data['state']
        )
        print('sending notification...')
        send_notification_request.delay(request_id=instance.id , notif_type=1)
        print('returning from serializers...')
        return instance
    
    def update(self , instance , validated_data):
        if self.context['request'].user == instance.file.createdBy:
            state = validated_data['state']
            instance.state = state
            if state == 1:
                print('assinging permission')
                file = File.objects.get(docId=validated_data['docId'])
                assign_perm('files.can_edit' , instance.from_user ,file )
            instance.save()
            return instance
        else:
            raise serializers.ValidationError('You are not the one who created this file and this cannot accept or reject a request')
        


class RequestNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['docId' , 'from_user' , 'id' , 'created_at' , 'state' , 'file']

    
