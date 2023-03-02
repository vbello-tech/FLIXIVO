from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from django.contrib.auth import authenticate, update_session_auth_hash
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage


# Create your views here.


def follow(request, pk):
    user = request.user
    person = get_object_or_404(UserProfile, pk=pk)
    user_prof =  get_object_or_404(UserProfile, person=user)
    if request.user != person.person:
        person.followers.add(user)
        user_prof.following.add(person.person)

    return HttpResponseRedirect(reverse("user:profile", kwargs={
            'pk':person.person.pk,
        }))


def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:login')
    else:
        form = NewUSerForm()

    context = {
        'form': form
    }
    return render(request, 'registrations/signup.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user:login')
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)

    context = {
        'form': form
    }
    return render(request, 'registrations/change_password.html', context)

class ProfileView(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(
                person=pk,
            )
            context = {
                'profile': profile
            }
            return render(self.request, 'registrations/user_detail.html', context)
        except ObjectDoesNotExist:
            return HttpResponse(request, 'THIS USER HAS NO PROFILE')

@login_required
def profile(request):
    person = request.user
    profile = UserProfile.objects.get(
        person=person,
    )
    context = {
        'profile': profile
    }
    return render(request, 'registrations/user_detail.html', context)

class ProfileUpdate(View):
    def get(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        context = {
            'form':form,
        }
        return render(request, 'registrations/profile_edit.html', context)
    def post(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(person=request.user,)
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES or None)
            if form.is_valid():
                tag = form.cleaned_data.get('tag')
                bio = form.cleaned_data.get('bio')
                profile_pic = form.cleaned_data.get('profile_pic')
                if tag:
                    profile.tag = tag
                if bio:
                    profile.bio = bio
                if profile_pic:
                    profile.profile_pic = profile_pic
                profile.save()
                return redirect('user:user-profile')
