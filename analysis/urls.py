from django.conf.urls import url, include

from analysis.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view()),

]