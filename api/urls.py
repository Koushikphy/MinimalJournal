from django.contrib import admin
from django.urls import path, re_path,include
from . import views
# from django.conf.urls import url, include
from rest_framework import routers

admin.site.site_header = 'Minimal Journal Admin Panel'

router = routers.DefaultRouter()
router1 = routers.DefaultRouter()
router.register('entries', views.EntryViewSets, basename='entries')



urlpatterns = [
    # home page route
    re_path(r'^$',views.index, name='home'),

    # route todo query api
    re_path('api/', include(router.urls)),


    # user registration api route
    path('register/', views.RegisterUserView.as_view()),

    # user login api route
    path('login/', views.LoginUserView.as_view()),

    # user logout api route
    path('logout/', views.logOutUser),


    path('listTags/',views.listTags)
]


