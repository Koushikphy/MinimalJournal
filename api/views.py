from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.utils.regex_helper import contains
from .serializers import LoginSerializer, RegistrationSerializer, ToDoSerializer, UserSerializer
from rest_framework import fields, serializers, viewsets
from .models import ToDos
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import api_view
from django.forms import ModelForm
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.utils.timezone import now
from django.utils import timezone
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView, ListAPIView



class customPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })





class ToDoViewSets(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ToDos.objects.all()
    serializer_class = ToDoSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    search_fields= ('desc','tags')
    filter_backends = (filters.SearchFilter,)
    pagination_class = customPagination
    def get_queryset(self):
        return ToDos.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # request.data[] = 
        print(request.data)
        ser = self.serializer_class(data=request.data)
        ser.is_valid()
        print(ser.errors)  # force to show errors
        return super().create(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        print(request.data)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        print(serializer.errors)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(["POST"])
def logOutUser(request):
    logout(request)
    return Response({"logout": "success"})


class RegisterUserView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # _, token = AuthToken.objects.create(user)
        # login(request, user)  # if you readily want to login the user after register
        return Response({
            "user" : UserSerializer(user, context=self.get_serializer_context()).data,
            # "token":token
        })


class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            messages.warning(request,"Invalid username, password")
            return Response({
                "error": "invalid username password"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = serializer.validated_data
            print(user,'==================')
            login(request, user)
            # messages.success(request, "Log in success")
            # _, token = AuthToken.objects.create(user)
            return Response({
                "user" : UserSerializer(user, context=self.get_serializer_context()).data,
                # "token":token
            })


# get the list of tags from the comma seperated string
@api_view(["GET"])
def listTags(request):
    queryset = ToDos.objects.values_list('tags')
    tags = {k.strip() for j in queryset for i in j for k in i.split(',')}
    return Response({'tags':tags})




def index(request):
    if(request.user.is_authenticated) :
        return render(request, 'index.html')
    else:
        return render(request, 'user.html')




from django.views.generic import ListView



class ContactListView(ListView):
    paginate_by = 2
    model = ToDos