from django.db import models
from django.core.exceptions import ValidationError
from datetime import date , time
import datetime

# now = datetime.datetime.now()

import re

# Create your models here.
#-- User Manager validation class
class UserManager(models.Manager):
    def user_validator(self, postData):
        errors ={}
        # First and Last Name validation
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name should be at least 3 characters long."
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last name should be at least 3 characters long."
            
        # Email validation    
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"   
        if len(postData['email']) < 10:
            errors['email'] = "Email should be at least 10 characters long."
            
        # Password validation    
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 4 characters long."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match!"
            
        return errors
#-- Session Manager validation class    
class SessionManager(models.Manager):
    def session_validator(self, postData):
        errors = {}
        #Artis/Band name validation
        if len(postData['artist_name']) < 1:
            errors['artist_name'] = "Artist name should be at least 2 character."
        #Session Date validation     
        try:
            session_date = postData['session_date']
            if not session_date:
                errors['session_date'] = "Session date is required."
            else:
                session_date_obj = date.fromisoformat(session_date)
                if session_date_obj < date.today():
                    errors['session_date'] = "Session date should be in the future."
        except ValueError:
            errors['session_date'] = "Invalid date format. Please use YYYY-MM-DD." 
            
            #Duration Validation
        # if len(int(postData['duration']))< 0:
        #     errors[int(postData['duration'])] = "Duration should be non zero number"
            
        if len(postData['genre']) < 3:
            errors['genre'] = "Genre should be at least 3 characters long."
        if len(postData['notes']) > 50 :
            errors['notes'] = "Notes should be maximum  50 characters long." 

        return errors
                

#--User Model Table
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
#-Session Model Table
class Session(models.Model):
    artist_name = models.CharField(max_length=100)
    session_date = models.DateField()
    duration = models.TimeField()
    genre = models.CharField(max_length=100)
    notes = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create_session', null= True, blank=True)
    supported_engineers = models.ManyToManyField(User, related_name = 'supporters')
    
    objects =SessionManager()
    
    def __str__(self):
        return f"{self.artist_name}m on {self.session_date}"
    
    
        

        
        
