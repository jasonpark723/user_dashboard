from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import bcrypt
import re
# Create your models here.


class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "first name: at least 2 characters required"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "last name: at least 2 characters required"
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha():
            errors['name'] = "invalid name"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'invalid email address!'
        for user in User.objects.all():
            if user.email == postData['email']:
                errors['email'] = "something went wrong!"
        if len(postData['password']) < 6:
            errors['password'] = "password must be longer than 5 characters"
        if postData['password'] != postData['password_ver']:
            errors['password'] = "password does not match!"
        return errors

    def login_validator(self, postData):
        pass

    def register(self, postData):
        user = User(
            first_name=postData['first_name'],
            last_name=postData['last_name'],
            email=postData['email'],

            password_hash=bcrypt.hashpw(
                postData['password'].encode(), bcrypt.gensalt())
        )
        user.save()
        return user

    def update_user(self, postData):


class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors = {}
        if not postData['message']:
            errors['message'] = "message cannot be blank!"
        return errors

    def create_message(self, postData, uid):
        message = Message(
            message=postData['message'],
            user=User.objects.get(id=postData['user_id']),
            author=User.objects.get(id=uid)
        )
        message.save()
        return message


class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        if not postData['comment']:
            errors['comment'] = "comment cannot be blank!"
        return errors

    def create_comment(self, postData, commenter_id):
        comment = Comment(
            comment=postData['comment'],
            user=User.objects.get(id=commenter_id),
            message=Message.objects.get(id=postData['message_id'])
        )
        comment.save()
        return comment


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_level = models.IntegerField(
        default=1, validators=[MaxValueValidator(9), MinValueValidator(1)])
    description = models.TextField(blank=True, default='')
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, blank=True, default='')
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # .messages show all the message about that user
    # .comments
    # .message show the message that user wrote


class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, related_name='messages')
    author = models.ForeignKey(
        User, related_name='written_message', null=True, blank=True)
    objects = MessageManager()
    # .comments


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='comments')
    message = models.ForeignKey(Message, related_name='comments')
    objects = CommentManager()
