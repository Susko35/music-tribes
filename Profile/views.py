from Profile.models import profile_info
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User

from .models import profile_info
from .forms import EditAccountForm
from .forms import RegisterUserForm

# Create your views here.


def home_view(request):

    return render(request, "home.html", {})

def register_view(request, *args, **kwargs):
    register_form=RegisterUserForm()

    if request.method== 'POST':
        register_form=RegisterUserForm(request.POST)
        if register_form.is_valid():
            user=register_form.save()
            profile_info.objects.create(
                user=user
            )
            messages.success(request, ('Account created successfully !'))
            return redirect('home')
        else:
            messages.error(request, 'Form was not filled properly !')
    context={"register_form":register_form}
    return render(request, "Profile/register.html",context)

def login_view(request, *args, **kwargs):
    
    if request.method=='POST':
        username=request.POST.get('username')
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('Logged in successfully !'))
            return redirect('home')
        else:
             messages.info(request, "Incorrect username or password")
    context={}
    return render(request, "Profile/login.html", context)


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('login')

def edit_user_view(request):
    my_profile = get_object_or_404(User, username=request.user)
    if request.method == 'POST':
        
        form = EditAccountForm(request.POST, request.FILES, instance=my_profile.profile_info)
        if  form.is_valid():
            form.save()
            messages.success(request, ('Account updated successfully !'))
            return redirect('home')
        
    else:
        form = EditAccountForm(instance=my_profile.profile_info)

    picture=my_profile.profile_info.profile_picture
    return render(request, 'Profile/edit_user.html', {
        'form': form,
        'picture':picture
    })