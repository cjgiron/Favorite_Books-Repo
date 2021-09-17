from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book
import bcrypt

def index(request):
    return render(request, "index.html")


def login_process(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/dashboard')


def register_process(request):
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)

        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )

        request.session['user_id'] = user.id
        return redirect('/dashboard')


def process_book(request):
    errors = Book.objects.book_validator(request.POST)
    user = User.objects.get(id = request.session['user_id'])

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/dashboard')
    else:
        book = Book.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            uploaded_by = user,
        )

        user.liked_books.add(book)
        return redirect('/dashboard')


def dashboard(request):
    if "user_id" not in request.session:
        return redirect('/')

    context = {
        'user': User.objects.get(id = request.session['user_id']),
        'all_books': Book.objects.all(),
    }

    return render(request, 'dashboard.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')