from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate, update_session_auth_hash
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.


def follow(request, pk):
    user = request.user
    person = get_object_or_404(UserProfile, pk=pk)
    user_prof =  get_object_or_404(UserProfile, person=user)
    if user != person:
        person.followers.add(user)
        user_prof.following.add(person.person)

    return HttpResponseRedirect(reverse("user:profile", kwargs={
            'pk': person.pk,
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
        profile = UserProfile.objects.get(
            pk=pk,
        )
        context = {
            'profile': profile
        }
        return render(self.request, 'registrations/user_detail.html', context)

