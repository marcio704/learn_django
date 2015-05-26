from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^posts', views.posts, name='posts'),
    url(r'^about', views.about, name='about'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^send_contact', views.send_contact, name='send_contact'),
    url(r'^(?P<post_id>[0-9]+)/send_comment', views.send_comment, name='send_comment'),
    url(r'^send_answer_to_comment/(?P<post_id>[0-9]+)/(?P<comment_id>[0-9]+)/', views.send_answer_to_comment, name='send_answer_to_comment'),
    url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
]

"""
ex: /polls/5/
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
"""