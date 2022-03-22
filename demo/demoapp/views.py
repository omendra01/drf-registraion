from multiprocessing import context
from django.shortcuts import get_object_or_404, render
from itsdangerous import Serializer
from .models import *
from rest_framework import viewsets
from rest_framework.response import Response
from.serializers import *
from django.contrib.auth import authenticate
# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['user']=user.username
    refresh['mobile']=user.mobile

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class StudentViewSet(viewsets.ViewSet):
    serializer_class = StudentSerializers
    def list(self,request):
        queryset = Student.objects.all()
        serializer = StudentSerializers(queryset,many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer = StudentSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
           user= serializer.save()
        #    token=get_tokens_for_user(user)
        return Response({'data':serializer.data}) 


    def retrieve(self, request, pk=None):   
        queryset = Student.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = StudentSerializers(user)
        return Response(serializer.data)    


    def destroy(self,request,pk=None):
        queryset = Student.objects.all()
        data = get_object_or_404(queryset, pk=pk)
        try:
            data.delete()
            return Response({'status':'Records Delted Succressfuly'})
        except:
            return Response({'status':'Records Not Found'})


    def partial_update(self,request,pk=None):
        queryset = Student.objects.get(pk=pk)
        serializer = StudentSerializers(queryset,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)    


class UserloginViewset(viewsets.ViewSet):
    serializer_class=UserloginSeraializer
    def create(self,request):
      
        serializer = UserloginSeraializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer)
           
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username,password=password)
            print(user)
           
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Success'})
            else:
                return Response('Invalid Credencial')


class StudentProfileViewset(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    def list(self,request):
        serializer = StudentProfileSerializer(request.user)
        return Response(serializer.data)    


class UserChangePasswordViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated] 
     
    def create(self,request):
        serializer = ChangPaswordSerializers(data=request.data, context = {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Upadted'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)