from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, CreateUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages



class IndexView(View):

    form = LoginForm()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('analysis'))
        else:
            return render(request, 'login/index.html', {'form': self.form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('analysis'))
        else:
            messages.add_message(request, messages.ERROR, "Username and Password do not match")
            return redirect(reverse('login'))


class CreateUser(View):

    def get(self, request):
        form = CreateUserForm()
        return render(request, 'login/create.html', {'form': form})

    def post(self, request):
        # get form data
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form = form.cleaned_data
            if form['password'] != form['password_confirm']:
                messages.add_message(request, messages.ERROR, "Passwords do not match, please try again")
                return redirect(reverse('signup'))
            else:
                try:
                    new_user = User.objects.create_user(form['username'], form['email'], form['password'])
                    messages.add_message(request, messages.SUCCESS, "Account created, you may now login")
                    return redirect(reverse('login'))
                except:
                    messages.add_message(request, messages.ERROR, "Username already exists")
                    return redirect(reverse('signup'))

                return redirect(reverse('signup'))
        else:
            messages.add_message(request, messages.ERROR, "Invalid inputs")
            return redirect(reverse('signup'))

        return render(request, 'login/create.html', {'form': CreateUserForm()})

