from django.contrib import auth
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import GbuserLoginForm, GbuserCreationForm, GbuserChangeForm, GbuserProfileForm
from authapp.models import Gbuser, GbUserProfile


def login(request):
    redirect_to = request.GET.get('next', '')
    if request.method == 'POST':
        form = GbuserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            redirect_to = request.POST.get('redirect-to')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_to or reverse('general:home'))
    else:
        form = GbuserLoginForm()

    cont = {
        'page_title': 'login',
        'form': form,
        'redirect_to': redirect_to,
    }
    return render(request, 'authapp/login.html', cont)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('general:home'))


def register(request):
    if request.method == 'POST':
        form = GbuserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_activation_key()
            user.save()
            if not user.send_confirm_email():
                return HttpResponseRedirect(reverse('auth:register'))
            return HttpResponseRedirect(reverse('general:home'))
    else:
        form = GbuserCreationForm()

    cont = {
        'page_title': 'registration',
        'form': form,
        }
    return render(request, 'authapp/register.html', cont)


def edit(request):
    if request.method == 'POST':
        form = GbuserChangeForm(request.POST, request.FILES,
                                instance=request.user)
        profile_form = GbuserProfileForm(request.POST, request.FILES,
                                         instance=request.user.gbuserprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = GbuserChangeForm(instance=request.user)
        profile_form = GbuserProfileForm(instance=request.user.gbuserprofile)

    cont = {
        'page_title': 'Change Profile',
        'form': form,
        'profile_form': profile_form,
        }
    return render(request, 'authapp/update.html', cont)


def verify(request, email, activation_key):
    user = get_user_model().objects.filter(email=email).first()
    if user.activation_key == activation_key: # and not user.registered:
        user.is_active = True
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return render(request, 'authapp/verification.html')


@receiver(post_save, sender=Gbuser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        GbUserProfile.objects.create(user=instance)


@receiver(post_save, sender=Gbuser)
def save_user_profile(sender, instance, **kwargs):
    instance.gbuserprofile.save()
