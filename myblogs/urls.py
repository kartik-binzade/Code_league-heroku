from django.urls import path
from . import views
import django
from django.conf.urls import url
from django.urls import include, path

from myblogs import views
from django.contrib.auth.views import LogoutView
app_name = 'myblogs'

urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name='home'),
    path('home/<int:group_id>/', views.GroupView, name='group'),
    path('home/<int:group_id>/<int:class_id>/', views.ClassView, name='class'),
    path('blogposts/', views.blogposts, name= 'blogposts'),
    path('blogposts/<int:blogpost_id>/', views.blogpost, name= 'blogpost'),
    path('serves/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('Topics/',views.Topics, name = 'topics'),
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name= 'new_topic'),
    path('new_edits/<int:topic_id>/', views.new_edits, name='new_edits'),
    path('edit_edits/<int:edits_id>/', views.edit_edits, name='edit_edits'),
]
