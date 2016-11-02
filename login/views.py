from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.http import HttpResponse


# Create your views here.


class IndexView(View):

    form = LoginForm()

    def get(self, request):
        return render(request, 'login/index.html', {'form': self.form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/analysis/')
        else:
            return render(request, 'login/index.html', {'form': self.form, 'error':'Credentials are invalid'})



