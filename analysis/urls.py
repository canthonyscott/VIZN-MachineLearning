from django.conf.urls import url, include

from analysis.views import IndexView, HistoryView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='analysis'),
    url(r'^history/', HistoryView.as_view(), name='history'),

]