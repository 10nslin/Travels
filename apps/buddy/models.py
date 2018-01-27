from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
from datetime import datetime
# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


class UserManager(models.Manager):


    def validate_reg(self, post_data):
        errors = []
      
        if len(post_data['first_name']) < 3 or len(post_data['last_name']) < 3: #checking both first and last name that they have atleast 3 characters
            errors.append("name fields must be at least 3 characters")
       
        if len(post_data['password']) < 8: #validating character length with password input
            errors.append("password must be at least 8 characters")
    
        if not re.match(EMAIL_REGEX, post_data['email']): #validating email to make sure this a email. using Regex for formatting
            errors.append("invalid email")
      
        if len(User.objects.filter(email=post_data['email'])) > 0: #filtering database to see if email is there
            errors.append("email already in use")
      
        if post_data['password'] != post_data['password_confirm']: # confirming the characters entered in password and password confirm
            errors.append("passwords do not match")
        
        if not errors: #Creating new user
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5)) #hashing the password security
            new_user = self.create(
                first_name=post_data['first_name'], #post data is collectied from form with the name value and now is placed in db
                last_name=post_data['last_name'],
                email=post_data['email'],
                password=hashed #hashing password in db
            )
            return new_user
        return errors
        
    def validate_login(self, post_data):
        errors = []
        if len(self.filter(email=post_data['email'])) > 0: #checking db for email entered in login field
            user = self.filter(email=post_data['email'])[0] #if there grabbing the proper array value for the email and assigning the email to user
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()): #checking the hashed password in the db and encoding to see if they match.
                errors.append('email and/or password incorrect') 
        else:
            errors.append('email and/or password incorrect')

        if errors:
            return errors
        return user


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()
    def __str__(self):
        return self.first_name + self.last_name + self.email #formating the info so it dosen't jsut say object or value key


class TravelManager(models.Manager):
	def validate_travel(self, post_data):
		errors = []

		start_trip = datetime.strptime(post_data['start_trip'], '%Y-%m-%d').date()		
		end_trip = datetime.strptime(post_data['end_trip'], '%Y-%m-%d').date()
		#checking to make sure entries are made
		if len(post_data['destination']) < 1:
			errors.append("You must enter a destination")

		if len(post_data['plan']) < 1:
			errors.append("You must enter a plan")

		if len(post_data['start_trip']) < 1:
			errors.append("Start date cannot be blank")

		if len(post_data['end_trip']) < 1:
			errors.append("End date cannot be blank")

		if start_trip< datetime.today().date():
			errors.append('Start date must be in the future')
		if end_trip < start_trip:
			errors.append('End date must be after the start date')

		
		return errors

	def createTravel(self, post_data, user):
		travel = Travel.objects.create(
				destination = post_data['destination'],
				start_trip = post_data['start_trip'],
				end_trip = post_data['end_trip'],
				plan = post_data['plan'],
				user = user
			)

		user.travelers.add(travel)
		
		return travel

class Travel(models.Model):
	destination = models.CharField(max_length=255)
	start_trip = models.DateTimeField()
	end_trip = models.DateTimeField(max_length=255)
	plan = models.TextField()
	user = models.ForeignKey(User, related_name='trips')
	joined_by = models.ManyToManyField(User, related_name="travelers")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = TravelManager()
