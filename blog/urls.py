from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all_posts', views.all_posts, name='all_posts'),
    url(r'^about', views.about, name='about'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^send_contact', views.send_contact, name='send_contact'),
    url(r'^posts/(?P<post_url>\w+-?\w*)/send_comment', views.send_comment, name='send_comment'),
    url(r'^send_answer_to_comment/(?P<post_url>\w+-?\w*)/(?P<comment_id>[0-9]+)/', views.send_answer_to_comment, name='send_answer_to_comment'),
    url(r'^posts/(?P<post_url>\w+-?\w*)/$', views.detail, name='detail'),
    url(r'^login', views.login, name='login'),
    url(r'^auth', views.auth, name='auth'),
    url(r'^sign_in', views.sign_in, name='sign_in'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^forgot_password', views.forgot_password, name='forgot_password'),
    url(r'^(?P<category_id>[0-9]+)/posts_by_category', views.posts_by_category, name='posts_by_category'),
    url(r'^rescue_password', views.rescue_password, name='rescue_password'),
    url(r'^account_confirmation', views.account_confirmation, name='account_confirmation'),
    url(r'^find_post_by_content', views.find_post_by_content, name='find_post_by_content'),
]

"""
ex: /polls/5/
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
"""