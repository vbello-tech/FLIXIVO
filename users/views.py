from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate, update_session_auth_hash
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.


def follow(request, pk):
    user = request.user
    person = get_object_or_404(UserProfile, pk=pk)
    if user != person:
        person.followers.add(user)
    return redirect('blog:home')


def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('account:login')
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
            return redirect('food:home')
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)

    context = {
        'form': form
    }
    return render(request, 'registrations/change_password.html', context)

def user_edit(request, pk):
    d_user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=d_user)
        if form.is_valid:
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('account:user_detail', pk=user.pk)
        form = EditUserForm()
    else:
        form = EditUserForm(instance=d_user)

    context = {
        'form': form
    }
    return render(request, 'registrations/user_edit.html', context)


class ProfileView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        profile = UserProfile.objects.filter(
            person=self.request.user,
        )
        context = {
            'profile': profile
        }
        return render(self.request, 'registrations/user_detail', context)

