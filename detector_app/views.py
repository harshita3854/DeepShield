from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ImageUploadForm
from .models import UserUpload
from .utils import predict_image
import os

def home(request):
    return render(request, 'detector_app/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'detector_app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'detector_app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')

@login_required
def dashboard(request):
    uploads = UserUpload.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'detector_app/dashboard.html', {'uploads': uploads})

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            
            # Perform mock prediction
            image_path = upload.image.path
            prediction, confidence = predict_image(image_path)
            
            upload.prediction = prediction
            upload.confidence = confidence
            upload.save()
            
            return redirect('result', upload_id=upload.id)
    else:
        form = ImageUploadForm()
    return render(request, 'detector_app/upload.html', {'form': form})

@login_required
def result(request, upload_id):
    upload = get_object_or_404(UserUpload, id=upload_id, user=request.user)
    return render(request, 'detector_app/result.html', {'upload': upload})
