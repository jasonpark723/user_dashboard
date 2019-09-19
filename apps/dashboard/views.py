from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import User, Message, Comment
from django.contrib import messages
from django.contrib.messages import get_messages  # get messages
import bcrypt


def index(request):

    return render(request, 'index.html')


def signin(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    return render(request, 'signin.html')


def register(request):
    return render(request, 'register.html')


def create_user(request):
    if request.method == "POST":
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="signup")
            if 'id' not in request.session:
                return redirect('/register')
            else:
                return redirect('/users/new')
        new_user = User.objects.register(request.POST)
        if 'id' not in request.session:
            request.session['id'] = new_user.id
        return redirect('/dashboard')


def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password_hash.encode()):
                request.session['id'] = logged_user.id
                return redirect('/dashboard')
        messages.error(request, "Login failed. Try again", extra_tags='login')
    return redirect('/signin')


def logout(request):
    # del request.session['id']
    request.session.clear()
    return redirect('/')


def home(request):
    if 'id' not in request.session:
        return redirect('/signin')
    all_users = User.objects.all()
    context = {
        'users': all_users,
        'logged_user': User.objects.get(id=request.session['id'])
    }
    print(User.objects.get(id=request.session['id']).user_level)
    return render(request, "home.html", context)


def add_user(request):
    if 'id' not in request.session:
        return redirect('/signin')
    user_level = User.objects.get(id=request.session['id']).user_level
    if user_level != 9:
        print(request.session['id'])
        messages.error(
            request, "Only admin is able to add new users", extra_tags='admin_only')
        return redirect('/dashboard')
    return render(request, 'add_user.html')


def show_user(request, id):
    if 'id' not in request.session:
        return redirect('/signin')
    context = {
        'user': User.objects.get(id=id),
    }
    return render(request, 'show_user.html', context)


def edit_user(request, id):
    if 'id' not in request.session:
        return redirect('/signin')
    context = {
        "user": User.objects.get(id=id),
    }
    return render(request, 'edit_user.html', context)


def update_user(request, id):
    if 'id' not in request.session:
        return redirect('/signin')
    if request.method == "POST":
        updated_user = User.objects.filter(id=id).first()
        if updated_user:
            if 'password' in request.POST:
                if request.POST['password'] != request.POST['password_ver']:
                    messages.error(request, "password dont match",
                                   extra_tags='password_fail')
                    return redirect('/users/edit/'+id)
                updated_user.password_hash = bcrypt.hashpw(
                    request.POST['password'].encode(), bcrypt.gensalt())
                updated_user.save()
                return redirect('/users/show/'+id)
            updated_user.first_name = request.POST['first_name']
            updated_user.last_name = request.POST['last_name']
            updated_user.email = request.POST['email']
            updated_user.user_level = int(request.POST['user_level'])
            updated_user.save()
        return redirect('/users/show/'+id)


def delete_user(request, id):
    if 'id' not in request.session:
        return redirect('/signin')
    delete_user = User.objects.filter(id=id).first()
    if delete_user:
        delete_user.delete()
    return redirect('/dashboard')


def new_message(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        errors = Message.objects.message_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="message")
            return redirect('/users/show/'+str(user_id))
        new_message = Message.objects.create_message(
            request.POST, request.session['id'])
        print(new_message.user.messages.all())
        return redirect('/users/show/'+str(user_id))


def new_comment(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        errors = Comment.objects.comment_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="comment")
            return redirect('/users/show/'+str(user_id))
        new_comment = Comment.objects.create_comment(
            request.POST, request.session['id'])
        print(new_comment.user.messages.all())
        return redirect('/users/show/'+str(user_id))


def edit_profile(request):
    pass
