from rest_framework import serializers
from .models import Notification
from django.utils.module_loading import import_string


class NotificationSerializer(serializers.ModelSerializer):

    serialized_object = serializers.SerializerMethodField()


    class Meta:
        model = Notification
        fields = ['message', 'serialized_object' , 'unread'  ,'notif_type' , 'id']


    def get_serialized_object(self , instance):
        if isinstance(instance , (Notification,)):
            object_app = instance.content_type.app_label
            object_name : str = instance.content_type.model
            serializer_module_path = f'{object_app}.serializers.{object_name}.{object_name.capitalize()}NotificationSerializer'
            serializer_class = import_string(serializer_module_path)
            model_module_path = f"{object_app}.models.{object_name.lower()}.{object_name.capitalize()}"
            model_class = import_string(model_module_path)
            instance =  model_class.objects.get(id=instance.content_object.id)
            serialized_model = serializer_class(instance)
        else:
            object_app = self.instance.content_type.app_label
            object_name : str = self.instance.content_type.model
            serializer_module_path = f'{object_app}.serializers.{object_name}.{object_name.capitalize()}NotificationSerializer'
            serializer_class = import_string(serializer_module_path)
            model_module_path = f"{object_app}.models.{object_name.lower()}.{object_name.capitalize()}"
            model_class = import_string(model_module_path)
            instance =  model_class.objects.get(id=self.instance.content_object.id)
            serialized_model = serializer_class(instance)

        return serialized_model.data

