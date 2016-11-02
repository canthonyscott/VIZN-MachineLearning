from django.conf.urls import url, include

from login.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
]