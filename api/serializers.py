from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from django.db.models import fields
from django.db.models.fields import files
from rest_framework import serializers
from .models import Entries
# Create your views here.
from django.contrib.auth import authenticate, login



class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entries
        # fields = '__all__'
        exclude = ['user']

    def save(self, **kwargs):
        kwargs['user'] = self.context['request'].user
        return super().save(**kwargs)



# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ('username', 'email', 'id') #noqa
        # fields = '__all__'



class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ('username', 'email', 'id', 'password') #noqa
        extra_kwargs={'password':{
            'write_only' : True
        }}
        # fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        return user #super().create(validated_data)



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
        
            return user
        raise ValidationError("incorrect password")