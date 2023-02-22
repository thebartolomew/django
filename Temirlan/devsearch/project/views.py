from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request, username=username, password=password) 

        if user is not None:
            login(request, user)
            messages.success(request, 'User has logged in')
            return redirect('/')
        else:
            messages.error(request,'incorrect pasw')

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    messages.info(request,'User has logged out')
    return redirect('loginUser')

def registerUser(request):
    form = CustomUserCreationForm()
    context = {'form':form}
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request,'User has been created')
           username = form.cleaned_data['username']
           password = form.cleaned_data['password1']
           user = authenticate(username=username, password=password)
           login(request, user)
           return redirect('/')
        else:
            messages.error(request, 'Error')
    return render(request, 'register.html', context)


def main(request):
    return render(request, 'index.html')