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

# Create your views here.

#TODO: Implement category list as a tag lib.
def index(request):
    post_list = Post.objects.all().order_by('date')
    paginator = Paginator(post_list, 5)
    try:
        page = request.GET.get('page')
        posts_by_page = paginator.page(page)
    except PageNotAnInteger:
        posts_by_page = paginator.page(1)
    except EmptyPage:
        posts_by_page = paginator.page(paginator.num_pages)

    category_list_parts = utils.divide_list_by_two(Category.objects.all())
    context = {'post_list': posts_by_page, 'category_list_1': category_list_parts["list_1"], 'category_list_2': category_list_parts["list_2"]}
    
    return render(request, 'blog/index.html', context)

#TODO: Implement category list as a tag lib.
def detail(request, post_url):
    post = Post.objects.get(url=post_url)
    category_list_parts = utils.divide_list_by_two(Category.objects.all())
    context = {'post': post, 'category_list_1': category_list_parts["list_1"], 'category_list_2': category_list_parts["list_2"]}

    return render(request, "blog/post/detail.html", context)
    
    
def all_posts(request):
    post_list = Post.objects.all().order_by('-date')
    paginator = Paginator(post_list, 6)

    try:
        page = request.GET.get('page')
        posts_by_page = paginator.page(page)
    except PageNotAnInteger:
        posts_by_page = paginator.page(1)
    except EmptyPage:
        posts_by_page = paginator.page(paginator.num_pages)

    context = {'post_list': posts_by_page}
    return render(request, 'blog/post/all_posts.html', context)

def posts_by_category(request, category_id):
    post_list = Post.objects.filter(category=category_id).order_by('-date')
    paginator = Paginator(post_list, 3)

    try:
        page = request.GET.get('page')
        posts_by_page = paginator.page(page)
    except PageNotAnInteger:
        posts_by_page = paginator.page(1)
    except EmptyPage:
        posts_by_page = paginator.page(paginator.num_pages)

    category = Category.objects.get(pk=category_id)
    context = {'post_list': posts_by_page, 'category': category}

    return render(request, 'blog/post/posts_by_category.html', context)

def contact(request):
    return render(request, 'blog/contact.html')

def about(request):
    return render(request, 'blog/about.html')        

def send_contact(request):
    if request.method == 'POST':
        try:
            contact = Contact(name=request.POST.get('name'), email=request.POST.get('email'), message=request.POST.get('message'), creation_date=timezone.now())
            contact.save()
            return HttpResponse(200)
        except Exception as inst:
            print (type(inst))
            print ('Error on saving contact information: {0}'.format(inst))
            
            return HttpResponse(500)    
    else:
        return HttpResponseRedirect('/contact')

def forgot_password(request):
    if request.method == 'POST':
        to_email = ''
        try: 
            to_email = request.POST.get('email')
        except Exception as inst:
            return HttpResponse('email', status=500)
        try:
            user = User.objects.get(email=to_email)
        except Exception as inst:
            return HttpResponse('user', status=500)  
        if user is not None:
            try:
                token = TokenPassword.objects.get(user=user, is_used=False)
            except ObjectDoesNotExist as inst:
                token_value = utils.generate_token()
                token = TokenPassword(user=user, value=token_value)    
                token.save()
            try:
                msg = _("""
                    Hi, did you forget your EasyDjango password?

                    Click the link below to rescue your password:
                    """)

                link = "{0}/rescue_password?token={1}".format(settings.SITE_URL, token.value)
                utils.send_email(to_email, msg+link)
                return HttpResponse(200)    
            except Exception as inst:
                print ('Error on sending new password via email: {0}'.format(inst))
        
        return HttpResponse("forgot_password_error", status=500)  
    else:
        return render(request, 'blog/registration/forgot_password.html')    

@transaction.atomic
def rescue_password(request):
    if request.method == 'POST':
        try:
            token = request.POST.get('token')
            user_id = request.POST.get('user_id')
            password_1 = request.POST.get('password_1')
            password_2 = request.POST.get('password_2')
        except:
            return HttpResponse("missing_information", status=500)  
        if password_1 != password_2:
            return HttpResponse("wrong_password_confirmation", status=500)  

        user = User.objects.get(pk=user_id)
        user.password = make_password(password_1, salt=None, hasher='default')
        user.save()

        token_pass = TokenPassword.objects.get(value=token, is_used=False)
        token_pass.is_used = True
        token_pass.used_at = timezone.now()
        token_pass.save()

        return HttpResponse(200)  
    else:
        try:
            token_pass = TokenPassword.objects.get(value=request.GET.get('token'), is_used=False)
        except ObjectDoesNotExist as inst:
            return render(request, 'blog/registration/rescue_password.html',  {'invalid_token': True})            
        user = User.objects.get(pk=token_pass.user.id)
        return render(request, 'blog/registration/rescue_password.html',  {'token': token_pass, 'token_user': user})            

def login(request):
    try:
        next = request.GET.get('next')
    except Exception as inst:
        print (type(inst))
        print ('On login process: {0}'.format(inst))        
    
    next = '/' if next is None else '/posts/{0}/#comment-tab'.format(next.split('/')[2]) 
    return render(request, 'blog/registration/login.html', {'next': next})  

def logout(request):
    logout_auth(request)
    return HttpResponseRedirect('/')

def auth(request):
    if request.method == 'POST':
        try: 
            user = authenticate(username=request.POST.get('login-username'), password=request.POST.get('login-password'))
            if user is not None:
                try:
                    token = TokenUserSignIn.objects.get(user=user)
                except ObjectDoesNotExist as inst:
                    return render(request, 'blog/registration/login.html', {'invalidation': _('Confirmation token not found for this user')})                    
                
                if not token.is_used:
                    return render(request, 'blog/registration/login.html', {'invalidation': _('User not confirmed yet, get the confirmation link at your e-mail!')})                    
                
                login_auth(request, user)
                return HttpResponseRedirect(request.POST.get('login-next'))  
            else:
                return render(request, 'blog/registration/login.html', {'invalidation': _('User/password not found!')})                    
        except Exception as inst:
            print (type(inst))
            print ('Error on authenticating user: {0}'.format(inst))
            
            return render(request, 'blog/registration/login.html')    
    else:
        return HttpResponseRedirect('/')


def sign_in(request):
    try:
        return _sign_in(request)
    except Exception as inst:
        print ('Error on creating user: {0}'.format(inst))
        return render(request, 'blog/registration/sign_in.html', {'error': _('Sorry, an error occurred while creating  your user. Try again later.')})     

@transaction.atomic
def _sign_in(request):
    if request.method == 'POST':
        userProfileForm = UserProfileForm(request.POST, request.FILES or None)
        userForm = UserForm(request.POST or None)
        
        if userProfileForm.is_valid() and userForm.is_valid():
            user = userForm.save(commit=False)
            
            if not user.password == request.POST.get('password-confirmation'):
                userForm._errors['password'] = _('Wrong password confirmation')
                return render(request, 'blog/registration/sign_in.html', {'userProfileForm': userProfileForm, 'userForm':userForm})
            
            user.password = make_password(user.password, salt=None, hasher='default')
            user.save()

            user_profile = userProfileForm.save(commit=False)
            user_profile.user = user
            user_profile.save()

            try:
                token = TokenUserSignIn.objects.get(user=user, is_used=False)
            except ObjectDoesNotExist as inst:
                token_value = utils.generate_token()
                token = TokenUserSignIn(user=user, value=token_value)    
                token.save()
            
            msg = _("""Hi, just click the link below in order to confirm your EasyDjango account:

                    """)
            link = "{0}/account_confirmation?token={1}".format(settings.SITE_URL, token.value)
            utils.send_email(user.email, msg+link)    

            return render(request, 'blog/registration/sign_in.html', {'confirmation': _('Your account has been created, please go to your e-mail to confirm it.')})
        
        else:
            return render(request, 'blog/registration/sign_in.html', {'userProfileForm': userProfileForm, 'userForm':userForm})
    else:
        userProfileForm = UserProfileForm()
        userForm = UserForm()
        return render(request, 'blog/registration/sign_in.html', {'userProfileForm': userProfileForm, 'userForm':userForm})

def account_confirmation(request):
    if request.method == 'GET':
        try:
            token_pass = TokenUserSignIn.objects.get(value=request.GET.get('token'), is_used=False)
        except ObjectDoesNotExist as inst:
            return render(request, 'blog/registration/account_confirmation.html',  {'invalid_token': True})            
        
        user = User.objects.get(pk=token_pass.user.id)
        token_pass.is_used = True
        token_pass.used_at = timezone.now()
        token_pass.save()
        
        return render(request, 'blog/registration/account_confirmation.html',  {'token': token_pass, 'token_user': user}) 


@login_required
def send_comment(request, post_url):
    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user) 
            comment = Comment(text=request.POST.get('comment-text'), date=timezone.now(), author=user_profile, post=Post.objects.get(url=post_url))
            comment.save()
            return HttpResponseRedirect('/posts/{0}/#comment-tab'.format(post_url))
        except Exception as inst:
            print (type(inst))
            print ('Error on saving comment information: {0}'.format(inst))
            
            return HttpResponse(500)    
    else:
        return HttpResponseRedirect('/posts/{0}/'.format(post_url))

@login_required
def send_answer_to_comment(request, post_url, comment_id):
    if request.method == 'POST':
        try:
            answer_to = Comment.objects.get(pk=comment_id)
            user_profile = UserProfile.objects.get(user=request.user)
            comment = Comment(text=request.POST.get('answer-text-{0}'.format(comment_id)), date=timezone.now(), author=user_profile, post=Post.objects.get(url=post_url), answer_to=answer_to)
            comment.save()
            return HttpResponseRedirect('/posts/{0}/#comment-tab'.format(post_url))
        except Exception as inst:
            print (type(inst))
            print ('Error on saving answer information: {0}'.format(inst))
            
            return HttpResponse(500)    
    else:
        return HttpResponseRedirect('/posts/{0}/'.format(post_url))