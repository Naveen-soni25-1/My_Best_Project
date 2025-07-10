from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """ The Home Page for learning logs."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all Topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

""" A context is a dictionary in which the keys are names we’ll use in the template to access 
the data we want, and the values are the data we need to send to the template. """

@login_required
def topic(request, topic_id):
    """Show all information about a single topic."""
    topic = get_object_or_404(Topic, id=topic_id)

    # Make sure the topic belongs to the current user.
    if not check_topic_owner(topic, request.user):
        raise Http404  # Use raise, not return

    entries = topic.entry_set.order_by('date_added')  # '-' for newest first
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            # Assign the current user as the topic owner.
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add new entry for a topic"""
    topic = get_object_or_404(Topic, id=topic_id)

    if not check_topic_owner(topic, request.user):
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit entries."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    if not check_topic_owner(topic, request.user):
        raise Http404

    if request.method != 'POST':
        # initialize request:pre-fill fprm with current entry
        form = EntryForm(instance=entry)
    else:
        # post data submitted :process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id= topic.id )
    
    context = {'topic':topic, 'entry':entry, 'form':form }
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    """Delete a single entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if not check_topic_owner(topic, request.user):
        raise Http404

    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)

    return render(request, 'learning_logs/delete_entry_confirm.html', {'entry': entry})

@login_required
def delete_topic(request, topic_id):
    """Add a new topic"""
    topic = get_object_or_404(Topic, id=topic_id)

    if not check_topic_owner(topic, request.user):
        raise Http404

    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')
    
    return render(request, 'learning_logs/topic.html', {'topic':topic})

def check_topic_owner(topic, requesting_user):
    """Check if topic owner is same as requesting user"""
    return topic.owner == requesting_user