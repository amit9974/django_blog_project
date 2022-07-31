
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path("", views.home,name="home"),
    path('post_list/', views.post_list, name='post_list'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('post_details/<slug>', views.post_details, name='post_details'),
    path("<int:id>comments/", views.comments, name="comments"),


] 
