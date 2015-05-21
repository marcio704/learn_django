from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^posts', views.posts, name='posts'),
    url(r'^about', views.about, name='about'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
]

"""
ex: /polls/5/
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
"""