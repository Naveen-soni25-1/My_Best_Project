""" Definig URl for blog App"""

from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # page containning all blog title
    path('titles/', views.titles, name='titles'),
    # page containing individual topic
    path('title/<int:title_id>/', views.title, name='title'),
    # new topic view function
    path('new_title/', views.new_title, name='new_title'),
    # new post view function
    path('new_post/<int:title_id>/', views.new_post, name='new_post'),
    # delete  post view function
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    # delete title view function
    path('delete_title/<int:title_id>/', views.delete_title, name='delete_title'),
    # edit_post view function
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
]