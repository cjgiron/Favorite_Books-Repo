from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}

        # validate names
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name should be longer than two characters."
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name should be longer than two characters."

        # validate email
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        else:
            user_list = User.objects.filter(email = post_data['email'])
            if len(user_list) > 0:
                errors['email'] = "Email already in use."

        # validate password
        if len(post_data['password']) < 8:
            errors['password'] = "Password should be longer than 4 characters."
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = "Password and Confirm PW must match."
        return errors


    def login_validator(self, post_data):
        errors = {}

        user_list = User.objects.filter(email = post_data['email'])
        if len(user_list) > 0:
            user = user_list[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid Credentials"
        else:
            errors['email'] = "Invalid Credentials"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # liked_books = a list of books a given user likes
    # books_uploaded = a list of books uploaded by a given user


class BookManager(models.Manager):
    def book_validator(self, post_data):
        errors = {}

        if len(post_data['title']) < 1:
            errors['title'] = "Title is required."
        if len(post_data['description']) < 5:
            errors['description'] = "Description must be at least 5 characters."
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()