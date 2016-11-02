from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UploadForm

# Create your views here.


class IndexView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form = UploadForm()

    def get(self, request):
        return render(request, 'analysis/index.html', {'form': self.form})

    def post(self, request):
        file = request.FILES['file']
        #todo process file with scripts

        return HttpResponse(file)

