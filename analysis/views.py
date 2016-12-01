from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
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
        return render(request, 'analysis/index.html', {'form': self.form, 'nbar': 'analysis'})

    def post(self, request):
        file = request.FILES['file']
        filename = file.name
        result = testToModel_onefile(file)
        matched = match_to_plate_new(result['result'], result['skipped'], result['plate'])
        plate_size = result['plate']
        self.save_to_db(filename, matched, request.user, plate_size)
        return render(request, 'analysis/results2.html', {'matched':matched, 'plate_size': plate_size})

    def save_to_db(self, filename, matched, owner, plate_size):
        p_matched = pickle.dumps(matched)
        result = Result()
        result.results = p_matched
        result.filename = filename
        result.owner = owner
        result.plate_size = plate_size
        result.save()


class HistoryView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        # get any potential GET params
        ID = request.GET.get('id')

        if ID is not None:
            try:
                details = Result.objects.get(pk=ID, owner=request.user)
            except Result.DoesNotExist:
                raise PermissionDenied

            matched = pickle.loads(details.results)
            plate_size = details.plate_size
            return render(request, 'analysis/results2.html', {'matched':matched, 'plate_size':plate_size, 'item_id': ID})

        else:
            # no ID sent, display all
            histories = Result.objects.filter(owner=request.user)
            return render(request, 'analysis/history.html', {'histories': histories, 'nbar': 'history'})


class DeleteHistory(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        # delete the history and return to history view
        ID = request.POST.get('id',0)
        if ID:
            Result.objects.filter(pk=ID).delete()
            messages.add_message(request, messages.SUCCESS, 'Successfully Deleted History')
            return redirect(reverse('history'))

        else:
            return HttpResponseBadRequest
