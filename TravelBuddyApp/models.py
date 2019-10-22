from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors={}
        if len(postData['name']) < 3:
            errors['name'] = "Name must be at least three characters"
        if len(postData['username']) < 3:
            errors['username'] = "Username must be at least three characters"    
        if len(User.objects.filter(username=postData['username'])) > 0:
            errors['user'] = "This user already exists"
        if postData['password'] != postData['passwordconfirm']:
            errors['password'] = "The confirmed password is incorrect"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least eight characters"
        return errors

    def login_validator(self, postData):
        errors={}
        if len(postData['username']) < 3:
            errors['username'] = "Username must be at least three characters"
        elif len(User.objects.filter(username=postData['username'])) == 0:
            errors['user'] = "User does not exist"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least eight characters"
        elif len(User.objects.filter(username=postData['username'])) != 0:
            user = User.objects.get(username=postData['username'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()) == False:
                errors['password'] = "Password is incorrect"
        return errors

class DestinationManager(models.Manager):
    def trip_validator(self, postData):
        errors={}
        if len(postData['destination']) < 1 or len(postData['description']) < 1 or len(postData['traveldatefrom']) < 1 or len(postData['traveldateto']) < 1:
            errors['input'] = "All fields are required"
        elif datetime.strptime(postData['traveldatefrom'], "%Y-%m-%d") < datetime.today() or datetime.strptime(postData['traveldateto'], "%Y-%m-%d") < datetime.today():
            errors['date'] = "Dates must be in the future"
        elif datetime.strptime(postData['traveldatefrom'], "%Y-%m-%d") > datetime.strptime(postData['traveldateto'], "%Y-%m-%d"):
            errors['date'] = "Travel date to must be after travel date from"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Destination(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    traveldatefrom = models.DateField()
    traveldateto = models.DateField()
    users = models.ManyToManyField(User, related_name="destinations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DestinationManager()