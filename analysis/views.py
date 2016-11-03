from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UploadForm
from .scripts.NormalizedModelTesting import testToModel_onefile
from .scripts.preprocessor import match_to_plate_new
from .models import Result
import pickle
# Create your views here.


class IndexView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    form = UploadForm()

    def get(self, request):
        return render(request, 'analysis/index.html', {'form': self.form})

    def post(self, request):
        file = request.FILES['file']
        filename = file.name
        result = testToModel_onefile(file)
        matched = match_to_plate_new(result['result'], result['skipped'], result['plate'])
        plate_size = result['plate']
        self.save_to_db(filename, matched, request.user)
        return render(request, 'analysis/results2.html', {'matched':matched, 'plate_size': plate_size})

    def save_to_db(self, filename, matched, owner):
        p_matched = pickle.dumps(matched)
        result = Result()
        result.results = p_matched
        result.filename = filename
        result.owner = owner
        result.save()

