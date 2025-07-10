from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Register a new user"""
    if request.method !="POST":
        # create an blank registration form
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        # process the user registration 
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('blog:index')
        
    # create an blank or invalid form
    context = {"form":form}
    return render(request, 'registration/register.html', context)