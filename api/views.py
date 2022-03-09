import django
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.utils.regex_helper import contains
from rest_framework import fields, serializers, viewsets
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
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView, ListAPIView
from .models import Entries
from .serializers import LoginSerializer, RegistrationSerializer, EntrySerializer, UserSerializer





class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('tags'):
            return ['tags']
        else:
            return ['desc']


    def filter_queryset(self, request, queryset, view):
        qs = super().filter_queryset(request, queryset, view)

        # when only desc don't search through the tags
        if 'desc' in self.get_search_fields(view, request):
            # using walrus operator, requires python 3.8<
            if (searchTerms := self.get_search_terms(request)):
                print(f'#{searchTerms[0]}.*')
                qs = qs.exclude(desc__regex=f'#{searchTerms[0]}.*')

        return qs

    # In django search filter multiple parameter can be provided with comma, 
    # but that means the result has to have all the parameter present (`and` operation)
    # we can modify the `filter_queryset` method of the searchfilter to 
    # modify the `and` -> `or` operation to have any one of them present

    
# http://127.0.0.1:8000/api/entries/?search=new&tags=new # the last new does not matter



class customPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "pagination":{
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'current' : self.page.number,
                'count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
            },
            'results': data
        })





class EntryViewSets(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Entries.objects.all()
    serializer_class = EntrySerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    search_fields= ('desc','tags')
    filter_backends = (CustomSearchFilter,)
    pagination_class = customPagination

    
    
    def get_queryset(self):
        return Entries.objects.filter(user=self.request.user).order_by('-id')

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
# TODO: Impletment a Tags model and query list of tags from there
@api_view(["GET"])
def listTags(request):
    queryset = Entries.objects.values_list('tags')
    tags = {k.strip() for j in queryset for i in j for k in i.split(',')}
    tags = [x for x in tags if x]
    return Response({'tags':tags})




def index(request):
    if(request.user.is_authenticated) :
        return render(request, 'index.html')
    else:
        return render(request, 'user.html')

