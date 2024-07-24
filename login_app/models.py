from django.db import models
import re
import bcrypt
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

class UserManager(models.Manager):
    def basic_register(self, postData): # function for registration 
        errors = {}
        if len(postData['first_name']) < 2:# validated first name
            errors["first_name"] = "First Name should be at least 2 characters"## as list ""if satament
            # errors["first_name"].append=('')
        if len(postData['last_name']) < 2:# validated last name
            errors["last_name"] = "Last Name should be at least 2 characters"
        # validated dob to required in database and age grater than 13
        if not postData['dob']:
            errors["dob"] = "Date of Birth is required"
        else:
            # try:
                dob = datetime.strptime(postData['dob'], "%Y-%m-%d").date()
                today = datetime.now().date()
                age = today.year - dob.year
                if dob >= today:
                    errors["dob_past"] = "Date of Birth must be in the past"
                elif age < 13:
                    errors["dob"] = "Age must be at least 13 years"
        #validated format of mail and unique email used
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):             
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email=postData['email']).exists():
            errors['email_used'] = "Email already in use!"
        # validated pass to be greater than 8 char and match with confirm pass 
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors["confirm_pw"] = "Passwords are not match "
        return errors
    
    def basic_login(self, postData):# function for login 
            errors = {}
            try:
                user = User.objects.get(email=postData['email'])
            except ObjectDoesNotExist:
                errors['email'] = "Email not found."
                return errors
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid password."
            return errors



class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=225)
    dob = models.DateField(default=datetime.today) #
    password = models.CharField(max_length=50)
    confirm_pw=models.CharField(max_length=50)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# create user 
def create_user(POST):
    password = POST['password']
    return User.objects.create(
        first_name=POST['first_name'],
        last_name =POST['last_name'],
        email=POST['email'],
        dob=POST['dob'],
        password= bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
        # confirm_pw=POST['password']
        )

def get_user(session):
    return User.objects.get(id=session['user_id'])
