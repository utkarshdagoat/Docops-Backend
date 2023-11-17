from rest_framework import serializers
from myauth.models import User
from spaces.models.space import Space
from notifications.models import Notification


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'year' , 'display_picture' , 'email']





