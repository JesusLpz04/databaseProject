from django.shortcuts import render, redirect

from django.http import HttpResponse

from .forms import CreateUserForm,LoginForm, PostForm, CommentForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
from .models import Post, Comment,User, Message, Profile
from django.db.models import Q

from django.shortcuts import get_object_or_404
def home(request):

    # return HttpResponse('Hello, world!')
    return render(request, 'index.html')

def register(request):

    form= CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()
            return redirect("login")
    context ={
        'form': form
    }

    return render(request, 'register.html', context=context)


def my_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():

            username = request.POST.get('username')
            password= request.POST.get('password')

            user = authenticate(request, username= username , password=password)

            if user is not None:

                auth.login(request, user)

                #check if user has profile
                if hasattr(user, 'profile'):

                    return redirect("dashboard")
                else:
                    Profile.objects.create(
                    user=user,)
                    return redirect("dashboard")
    context ={
        'form': form
    }

    return render(request, 'login.html', context=context)

@login_required(login_url='login')
def dashboard(request):
    posts= Post.objects.all()
    user=request.user
    profile=user.profile
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        comment_id=request.POST.get("comment-id")
        follow=request.POST.get('follow-btn')
        if follow:
            profile.friends.add(follow)
        comment = Comment.objects.filter(id=comment_id).first()
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
        if comment and comment.name == request.user:
            comment.delete()
    context ={
        'posts': posts
    }
    return render(request, 'dashboard.html', context=context)


@login_required(login_url='login')   
def create_post(request):
    form = PostForm()
    if request.method =="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("dashboard")

    context ={
        'form': form
    }
    return render(request, 'create_post.html', context=context)

def comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.method =="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.name = request.user
            comment.post = post
            comment.save()
            return redirect("dashboard")

    context ={
        'form': form
    }
    return render(request, 'comment.html', context=context)

def friends(request):
    user=request.user
    profile=user.profile
    friends= profile.friends.all()
    if request.method == "POST":
        friend_id = request.POST.get("friend")
        friend = User.objects.filter(id=friend_id).first()
        print(friend)
        profile.friends.remove(friend)
    context ={
        'friends':friends,
        'user':user,
    }
    return render(request, 'friends.html', context=context)

def messages(request,pk):
    target_user = get_object_or_404(User, pk=pk)
    user= request.user
    # messages = Message.objects.filter(
    # msg_sender=user,
    # msg_receiver=target_user | msg_sender=target_user,
    # )
    condition_a = Q(msg_sender=user, msg_receiver=target_user)

    condition_b = Q(msg_sender=target_user, msg_receiver=user)

    messages = Message.objects.filter(condition_a | condition_b).order_by('id')
    if request.method == 'POST':
        message_body = request.POST.get('msg-txt') 

        if message_body:
            Message.objects.create(
                body=message_body,
                msg_sender=user, 
                msg_receiver=target_user 
            )
            
            return redirect('messages', pk=pk)
        
    context={
        'messages':messages
    }

    return render(request, 'messages.html', context=context)

def logout(request):

    auth.logout(request)

    return redirect("login")