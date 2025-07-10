from django.contrib import admin
from .models import Topic, Post

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin View for Topic"""
    list_display = ('title', 'is_active', 'date_added')
    list_filter = ['is_active', 'date_added']
    search_fields = ('title', 'description')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin View for Post"""
    list_display = ('title', 'topic' , 'date_added')
    list_filter = ['date_added']  
    search_fields = ('title', 'text')
