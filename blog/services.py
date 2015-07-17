#from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.contrib.auth import authenticate
from django.contrib.auth import  login as login_auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth.hashers import  make_password 
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.conf import settings
from django.db import transaction

from .models import Post
from .models import Category
from .models import Contact
from .models import UserProfile
from .models import Comment
from .models import TokenPassword
from .models import TokenUserSignIn

from .forms import UserProfileForm
from .forms import UserForm

from .utils import utils

import sys
import re
import tasks

def paginate(list, parts, page):
	paginator = Paginator(list, parts)
	try:
		posts_by_page = paginator.page(page)
	except PageNotAnInteger:
		posts_by_page = paginator.page(1)
	except EmptyPage:
		posts_by_page = paginator.page(paginator.num_pages)

	return posts_by_page

@transaction.atomic
def send_contact(name, email, message, creation_date):
	contact = Contact(name=name, email=email, message=message, creation_date=creation_date)
	contact.save()
	tasks.send_email.delay(settings.CLIENT_EMAIL, contact.get_contact_email_message())

def forgot_password(user):
	if user is not None:
		token = generate_password_token(user)
		msg = _("""
		Hi, did you forget your EasyDjango password?

		Click the link below to rescue your password:
		""")
		link = "{0}/rescue_password?token={1}".format(settings.SITE_URL, token.value)
		tasks.send_email.delay(user.email, msg+link)

def rescue_password(token, user_id,  password, password_confirmation):
	if password != password_confirmation:
		raise Exception('wrong_password_confirmation')

	user = User.objects.get(pk=user_id)
	encrypt_user_password(user, password)
	expire_password_token(token)
	

def expire_password_token(token):
	token_pass = TokenPassword.objects.get(value=token, is_used=False)
	token_pass.is_used = True
	token_pass.used_at = timezone.now()
	token_pass.save()

def generate_password_token(user):
	try:
		token = TokenPassword.objects.get(user=user, is_used=False)
	except ObjectDoesNotExist as inst:
		token_value = utils.generate_token()
		token = TokenPassword(user=user, value=token_value)    
		token.save()
	return token

def user_authentication(request, user, password):
	user = authenticate(username=user, password=password)
	if user is None:
		raise Exception('User/password not found!')
	try:
		token = TokenUserSignIn.objects.get(user=user)
	except ObjectDoesNotExist as inst:
		raise Exception('Confirmation token not found for this user')

	if not token.is_used:
		raise Exception('User not confirmed yet, get the confirmation link at your e-mail!')                 

	login_auth(request, user)

def expire_signin_token(token):
	try:
		token_signin = TokenUserSignIn.objects.get(value=token, is_used=False)
	except ObjectDoesNotExist as inst:
		raise Exception('invalid_token')            

	user = User.objects.get(pk=token_signin.user.id)
	token_signin.is_used = True
	token_signin.used_at = timezone.now()
	token_signin.save()

	return {'token': token_signin, 'token_user': user}

def generate_signin_token(user):
	try:
		token = TokenUserSignIn.objects.get(user=user, is_used=False)
	except ObjectDoesNotExist as inst:
		token_value = utils.generate_token()
		token = TokenUserSignIn(user=user, value=token_value)    
		token.save()
	return token

def send_comment(user, text, post):
	user_profile = UserProfile.objects.get(user=user) 
	comment = Comment(text=text, date=timezone.now(), author=user_profile, post=post)
	comment.save()

def send_answer_to_comment(comment_id, user, text, post):
	answer_to = Comment.objects.get(pk=comment_id)
	user_profile = UserProfile.objects.get(user=user)
	comment = Comment(text=text, date=timezone.now(), author=user_profile, post=post, answer_to=answer_to)
	comment.save()

def encrypt_user_password(user, password):
	user.password = make_password(password, salt=None, hasher='default')
	user.save()

def send_signin_email(token, email):
	msg = _("""Hi, just click the link below in order to confirm your EasyDjango account:

	        """)
	link = "{0}/account_confirmation?token={1}".format(settings.SITE_URL, token.value)
	tasks.send_email.delay(email, msg+link)