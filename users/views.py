from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'signup.html')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return render(request, 'signup.html')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'Account created successfully')
                    return render(request, 'signup.html')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'signup.html')
   
def sign_in(request):

    if request.method == 'POST':
        email  = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user) 
            messages.success(request, 'You are now logged in')
            return redirect('store')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
    return render(request, 'login.html')

@login_required(login_url='sign_in')
def profile(request):
    return render(request, 'my-account.html')

@login_required(login_url='sign_in')

def sign_out(request):
    logout(request)
    request.session.clear()
    messages.success(request, 'You are now logged out')
    return redirect('store')