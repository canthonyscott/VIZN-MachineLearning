from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, CreateUser
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.http import HttpResponse


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
            return render(request, 'login/index.html', {'form': self.form, 'error':'Credentials are invalid'})


class CreateUser(View):
     form = CreateUser()

     def get(self, request):
         return render(request, 'login/create.html', {'form': self.form})
