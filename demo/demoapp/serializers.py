from unicodedata import numeric
from django.forms import ValidationError
from rest_framework import serializers
from treq import request
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Student


#****************Student Create List Serializers***************

class StudentSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = ['id','username','course','mobile','password']


    def validate_mobile(self,value):
        if Student.objects.filter(mobile=value).exists():
            raise ValidationError('This Mobile Number Already Taken..')
        return value    

    # def validate_name(self,value):
    #     if value.isnumeric:
    #         raise ValidationError('Please Enter Valid Name')
    #     return value    
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(StudentSerializers, self).create(validated_data)


#****************Login Serializers**********************

class UserloginSeraializer(serializers.Serializer):
    username = serializers.CharField(max_length=255,style={
        'palceholder':'Enter Name'
    })
    password = serializers.CharField(max_length=255,style={
        'palceholder':'Enter password'
    }) 


# ************************Profile Serializers************

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','username','course','mobile','password']


#***************Change Password Serializers************************

class ChangPaswordSerializers(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    confirm_password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)

    class Meta:
        fields=['password','confirm_password']

# validate password and set new password

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')
        if password !=confirm_password:
            raise serializers.ValidationError('Password and Confirm password not match')
        user.set_password(password)
        user.save()    
        return attrs