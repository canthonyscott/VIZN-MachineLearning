from django.forms import forms


class UploadForm(forms.Form):
    file = forms.FileField()

