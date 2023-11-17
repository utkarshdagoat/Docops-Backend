from rest_framework import serializers
from files.models.file import File , FileText

from spaces.models.space import Space
from myauth.serializers.serializers import UserSerializers

from myauth.models import User

import uuid

from guardian.shortcuts import assign_perm

class FileSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    space = serializers.CharField(max_length=32, )
    invite_code = serializers.UUIDField(read_only=True )
    creater = UserSerializers(read_only=True)
    class Meta:
        model = File
        fields = ['cover' ,'creater', 'space' , 'isPrivate' , 'invite_code' , 'heading' , 'docId']

    def create(self,validated_data):
        name = validated_data['space']
        space = Space.objects.get(name=name)
        validated_data['space'] = space
        if self.context['request'].user.has_perm('can_create_file' , space):
            validated_data['createdBy'] = self.context['request'].user
            validated_data['inviteCode'] = uuid.uuid4()
            instance = File.objects.create(**validated_data)
            assign_perm('files.can_edit' , self.context['request'].user , instance)
            assign_perm('files.can_comment' , self.context['request'].user , instance)
            return instance
        else:
            raise serializers.ValidationError('You cannot create a file ask for permission  again')




class FileRetriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['cover' , 'heading' ]



class HeadingFileSerializer(serializers.Serializer):
    heading = serializers.CharField(max_length=200)


    def update(self,instance,validated_data):
        heading = validated_data['heading']
        instance.heading = heading
        instance.save()
        return instance


class CoverFileSerializer(serializers.Serializer):
    cover = serializers.ImageField()

    def update(self,instance,validated_data):
        cover = validated_data['cover']
        instance.cover = cover
        instance.save()
        return instance



class FileSpaceShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['heading' , 'docId']

class FileTextSerializer(serializers.ModelSerializer):
    file = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model=FileText
        fields = ['file' , 'text']
    
    def update(self , instance , validated_data):
        instance.text = validated_data['text']
        instance.save()
        return instance

class FileSearchSerializer(serializers.ModelSerializer):
    space = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = [ 'heading' , 'docId' , 'text' , 'space']
    
    def get_space(self , obj):
        return obj.space.name

class FilePermissionSerializer(serializers.ModelSerializer):
    edit_permission = serializers.SerializerMethodField()
    comment_permission = serializers.SerializerMethodField()

    
    class Meta:
        model = File
        fields = ['edit_permission' , 'comment_permission']

    def get_edit_permission(self , instance):
        return self.context['request'].user.has_perm('can_edit' , instance)
    
    def get_comment_permission(self, instance):
        return self.context['request'].user.has_perm('can_comment' , instance)
    
