from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')  # Get the raw (plain text) password
            user = authenticate(username=username, password=raw_password)  # Authenticate with the raw password
            if user is not None:
                login(request, user)
                messages.success(request, f'Account created for {username}!')
                return redirect('login')
            else:
                messages.error(request, 'An error occurred while creating your account. Please try again.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# # Create your views here.

# def register(request):
#     title = "Register"
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)

#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account Created! You can now login')
#             return redirect('login')

#     else:
#         form = UserRegisterForm()
#         title = "Register"
#     return render(request,'users/register.html',{ 'form': form },{'title': title})
    

@login_required
def profile(request):
    return render(request, 'users/profile.html')