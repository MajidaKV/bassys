from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .forms import User
from django.contrib import messages

from .forms import CreateUserForm

# Create your views here.
def home(request):
    if 'username' in request.session:
        return render(request,'home.html')
    return redirect('login')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'account was created for '+ user)
                return redirect('login')
        
        context = {'form':form}
        return render(request,'register.html',context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
               request.session['username'] = username
               login(request, user)
               return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request,'login.html',context)


def logoutUser(request):
    if 'username' in request.session:
        request.session.flush()     
    return redirect('login')




