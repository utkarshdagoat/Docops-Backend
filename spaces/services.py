from django.contrib.auth.models import Permission

from rest_framework import serializers

from guardian.shortcuts import assign_perm


from myauth.serializers.serializers import UserSerializers

from .models.space import Space
from .models.request import Request
from myauth.models import User
import uuid
from constants.constants import REQUEST_STATE
import redis

from .tasks import send_notification_request

def IsUserInSpace(obj:Space ,user:User) -> bool:
    '''
    Checks if user is in the space

    :params obj: Takes in the space object to check angaist , user:Takis in the user requested
    :type obj:Space , user: User

    :rtype: bool
    :return True if user is in the space and False otherwise
    '''
    if obj in User.objects.get(pk=user.id).space_set.all() or obj.creater == user :
        return True
    return False



def doesSpaceNameExist(name:str) -> bool:
    '''
    Checks if a space exist with a  name

    :params name: The name of the space
    :type name:str

    :rtype bool
    :return True if space exists and False otherwies
    '''
    try:
        space = Space.objects.filter(name=name)
        return True
    except:
        return False

def PublicSpaceInstanceFromContext(context : dict , validated_data:dict) -> Space:
    """
    Creates a space instance from context and validated_data passed in the serializer

    Args:
        context (dict): The context dictionary passed into the serializer
        validated_data (dict): The validated_data passed into the Serializer

    Returns:
        Space: Creates a Space instance with creater of the instance as the user in request
    """
    validated_data['creater'] =  context['request'].user
    # grant creater write permission
    instance = Space.objects.create(**validated_data)
    grantCreateFilePermission(user=context['request'].user , space=instance)
    return instance


def PivateSpaceInstanceFromContext(context : dict , validated_data:dict) -> Space:
    validated_data['creater'] =  context['request'].user 
    
    validated_data['isPrivate'] = True
    grantCreateFilePermission(user=context['request'].user)
    instance = Space.objects.create(**validated_data)
    return instance


def RequestInstanceForSendingRequest(context: dict , validated_data : dict) -> Request:
    user = context['request'].user
    validated_data['from_user'] = user
    invite_code = uuid.UUID(validated_data['invite_code'])
    space = Space.objects.get(invite_code=invite_code)
    validated_data['space'] = space
    validated_data['state'] = REQUEST_STATE[0]
    validated_data['creator'] = space.creater
    print('Creating Request....')
    instance = Request.objects.create(space=validated_data['space'] , from_user=user , state=validated_data['state'])
    print('Sending Notification....')
    send_notification_request.delay(request_id=int(instance.id) , notif_type=0)
    return instance



def updateRequestInstance(context:dict , instance : Request , validated_data:dict) -> Request:
    user = context['request'].user
    space = instance.space
    
    if space.creater != user:
        raise serializers.ValidationError('You are not the creater')
    
    state = validated_data['state']
    
    print(validated_data)

    if state == 'accepted':
        user = instance.from_user
        permission = validated_data['permission']
        print('accepted')
        if permission:
            print('permission giver')
            grantCreateFilePermission(user=user , space=space)
        space.users.add(user)
    
    instance.state = state
    
    instance.save()
    
    return instance


def grantCreateFilePermission(user:User , space:Space):
    assign_perm('can_create_file' , user , space)
        