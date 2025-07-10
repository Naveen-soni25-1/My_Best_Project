from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Post
from .forms import TopicForm, PostForm  # Add the dot for local import

def index(request):
    """Render home page"""
    return render(request, 'blog/index.html')

@login_required
def titles(request):
    """View to display all blog titles"""
    titles = Topic.objects.all()
    context = {'titles':titles}
    return render(request, 'blog/titles.html', context)

@login_required
def title(request, title_id):
    """View to display posts for a single title"""
    title = get_object_or_404(Topic, id=title_id)
    posts = title.post_set.order_by('date_added')
    context = {'title': title, 'posts': posts}
    return render(request, 'blog/title.html', context)

@login_required
def delete_post(request, post_id):
    """Delete a post (topic owner or admin only)"""
    post = get_object_or_404(Post, id=post_id)
    topic = post.topic

    if not (topic.owner == request.user or request.user.is_superuser or post.author == request.user):
        raise Http404

    if request.method == 'POST':
        post.delete()

    return redirect('blog:title', title_id=topic.id)


@login_required
def delete_title(request, title_id):
    """Delete an individual blog title"""
    title = get_object_or_404(Topic, id=title_id)

    if request.method == 'POST':
        if title.owner == request.user:  # Correct attribute and comparison
            title.delete()
            return redirect('blog:titles')
    # If not POST or user is not the owner, redirect or return 403
    return redirect('blog:titles')

@login_required
def new_title(request):
    """Add a new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)   # ✅ <-- Add this!
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('blog:titles')

    context = {'form': form}
    return render(request, 'blog/new_title.html', context)


@login_required
def new_post(request, title_id):
    """Add a new post to a topic"""
    topic = get_object_or_404(Topic, id=title_id)

    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.topic = topic  
            new_post.author = request.user 
            new_post.save()
            return redirect('blog:title', title_id=topic.id)

    context = {'title': topic, 'form': form}
    return render(request, 'blog/new_post.html', context)


@login_required
def edit_post(request, post_id):
    """Edit a post (only your own)"""
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user and post.topic.owner != request.user and not request.user.is_superuser:
        raise Http404

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:title', title_id=post.topic.id)

    context = {'title': post.title, 'post': post, 'form': form}
    return render(request, 'blog/edit_post.html', context)
