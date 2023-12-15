from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def home(request):
    blog_posts = BlogPost.objects.order_by('-date_added')
    current_year = datetime.now().year
    return render(request, 'blogs/home.html', {'blog_posts': blog_posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            # Свяжите текущего пользователя с создаваемой записью
            form.instance.author = request.user
            form.save()
            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'blogs/create_post.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)

    # Проверьте, что текущий пользователь - автор записи
    if post.author == request.user:
        post.delete()
    return redirect('home')


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)

    # Проверьте, что текущий пользователь - автор записи
    if post.author == request.user:
        if request.method == 'POST':
            form = BlogPostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = BlogPostForm(instance=post)
        return render(request, 'blogs/edit_post.html', {'form': form})
    else:
        return redirect('home')


def user_logout(request):
    logout(request)
    return redirect('home')
