from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from rest_framework import viewsets, permissions
from .models import User, Token
from .serializers import UserSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

def reset_password_link(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user found with that email address.')
            return redirect('forgot-password')

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(reverse('reset-password', kwargs={'uidb64': uid, 'token': token}))

        send_mail(
            'Password Reset Request',
            f'Please click the link below to reset your password:\n{reset_link}',
            'rexsum420@gmail.com',
            [email],
            fail_silently=False,
        )

        messages.success(request, 'A password reset link has been sent to your email.')
        return redirect('login')
    return render(request, 'forgot_password.html', {'authenticated': request.user.is_authenticated})

def login_view(request):
    next_url = request.GET.get('next', 'home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            next_url = request.POST.get('next', 'home')  # Get next_url from POST data
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'next': next_url})

def register(request):
    next_url = request.GET.get('next', 'home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            next_url = request.POST.get('next', 'home')  # Get next_url from POST data
            return redirect(next_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form, 'next': next_url})

def logout_view(request):
    auth_logout(request)
    return redirect('home')

class IsAuthenticatedOrCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrCreate]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

def reset_password(request, uidb64=None, token=None):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('reset-password', uidb64=uidb64, token=token)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'Invalid password reset link.')
            return redirect('forgot-password')

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Invalid password reset link.')
            return redirect('forgot-password')

    if uidb64 and token:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'reset_password.html', {'authenticated': request.user.is_authenticated})

    messages.error(request, 'Invalid password reset link.')
    return redirect('forgot-password')
