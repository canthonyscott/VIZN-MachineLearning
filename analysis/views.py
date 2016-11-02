from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UploadForm
from .scripts.NormalizedModelTesting import testToModel_onefile
from .scripts.preprocessor import match_to_plate_new
# Create your views here.


class IndexView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form = UploadForm()

    def get(self, request):
        return render(request, 'analysis/index.html', {'form': self.form})

    def post(self, request):
        file = request.FILES['file']
        result = testToModel_onefile(file)
        matched = match_to_plate_new(result['result'], result['skipped'], result['plate'])
        plate_size = result['plate']

        return render(request, 'analysis/results2.html', {'matched':matched, 'plate_size': plate_size})

