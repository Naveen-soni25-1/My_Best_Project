""" Defines URL pattern for learning logs."""

from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    # Detail page for a single topic.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # new topic for user
    path('new_topic/', views.new_topic, name='new_topic'),
    # new entries for topic
    path('new_entries/<int:topic_id>/', views.new_entry, name='new_entry'),
    # edit entries
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # delet an entry
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    # delete an topic
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic')
]