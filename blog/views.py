#from django.template import RequestContext, loader
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
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
from .elastic import ElasticSearchClient

import sys
import re
import tasks
import services

# Create your views here.

#TODO: Implement category list as a tag lib.
def index(request):
    post_list = services.paginate(Post.objects.all().order_by('date'), 5, request.GET.get('page'))
    category_list_parts = utils.divide_list_by_two(Category.objects.all())
    context = {'post_list': post_list, 'category_list_1': category_list_parts["list_1"], 'category_list_2': category_list_parts["list_2"]}
    return render(request, 'blog/index.html', context)

#TODO: Implement category list as a tag lib.
def detail(request, post_url):
    post = Post.objects.get(url=post_url)
    category_list_parts = utils.divide_list_by_two(Category.objects.all())
    context = {'post': post, 'category_list_1': category_list_parts["list_1"], 'category_list_2': category_list_parts["list_2"]}
    return render(request, "blog/post/detail.html", context)
    
    
def all_posts(request):
    post_list = services.paginate(Post.objects.all().order_by('-date'), 6, request.GET.get('page'))
    return render(request, 'blog/post/all_posts.html', {'post_list': post_list})

def posts_by_category(request, category_id):
    post_list = services.paginate(Post.objects.filter(category=category_id).order_by('-date'), 3, request.GET.get('page'))
    category = Category.objects.get(pk=category_id)
    return render(request, 'blog/post/posts_by_category.html', {'post_list': post_list, 'category': category})

def find_post_by_content(request):
    post_list = ElasticSearchClient().search_post_by_match(request.POST.get('term'))
    return render(request, 'blog/post/search_posts.html', {'post_list': post_list})

def contact(request):
    return render(request, 'blog/contact.html')

def about(request):
    return render(request, 'blog/about.html')        

def send_contact(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/contact')
    
    services.send_contact(request.POST.get('name'), request.POST.get('email'), request.POST.get('message'), timezone.now())
    return HttpResponse(200)
        
def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'blog/registration/forgot_password.html')

    try: 
        to_email = request.POST.get('email')
    except Exception as inst:
        return HttpResponse('email', status=500)
    try:
        user = User.objects.get(email=to_email)
    except Exception as inst:
        return HttpResponse('user', status=500)  
    try:
        services.forgot_password(user)
        return HttpResponse(200)    
    except Exception as inst:
        print(inst)
        return HttpResponse("forgot_password_error", status=500)  
        
@transaction.atomic
def rescue_password(request):
    if request.method == 'GET':
        try:
            token_pass = TokenPassword.objects.get(value=request.GET.get('token'), is_used=False)
        except ObjectDoesNotExist as inst:
            return render(request, 'blog/registration/rescue_password.html',  {'invalid_token': True})            
        user = User.objects.get(pk=token_pass.user.id)
        return render(request, 'blog/registration/rescue_password.html',  {'token': token_pass, 'token_user': user}) 
    
    try:
        token = request.POST.get('token')
        user_id = request.POST.get('user_id')
        password = request.POST.get('password_1')
        password_confirmation = request.POST.get('password_2')
    except:
        return HttpResponse("missing_information", status=500)  
    try:
        services.rescue_password(token, user_id, password, password_confirmation)
    except Exception as inst:
        return HttpResponse(inst, status=500)  

    return HttpResponse(200)  
                   

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
    if request.method == 'GET':
        return HttpResponseRedirect('/')
    try: 
        services.user_authentication(request, request.POST.get('login-username'), request.POST.get('login-password'))
        return HttpResponseRedirect(request.POST.get('login-next'))
    except Exception as inst:
        return render(request, 'blog/registration/login.html', {'invalidation': _(unicode(inst))})

def sign_in(request):
    try:
        return _sign_in(request)
    except Exception as inst:
        print ('Error on creating user: {0}'.format(inst))
        return render(request, 'blog/registration/sign_in.html', {'error': _('Sorry, an error occurred while creating  your user. Try again later.')})     

@transaction.atomic
def _sign_in(request):
    if request.method == 'GET':
        userProfileForm = UserProfileForm()
        userForm = UserForm()
        return render(request, 'blog/registration/sign_in.html', {'userProfileForm': userProfileForm, 'userForm':userForm})

    userProfileForm = UserProfileForm(request.POST, request.FILES or None)
    userForm = UserForm(request.POST or None)
    
    if not userProfileForm.is_valid() or not userForm.is_valid():
        return render(request, 'blog/registration/sign_in.html', {'userProfileForm': userProfileForm, 'userForm':userForm})
    
    user = userForm.save(commit=False)
    
    if not user.password == request.POST.get('password-confirmation'):
        userForm._errors['password'] = _('Wrong password confirmation')
        return render(request, 'blog/registration/sign_in.html', {'userProfileForm': userProfileForm, 'userForm':userForm})
    
    services.encrypt_user_password(user, user.password)

    user_profile = userProfileForm.save(commit=False)
    user_profile.user = user
    user_profile.save()

    token = services.generate_signin_token(user)
    services.send_signin_email(token, user.email)
    return render(request, 'blog/registration/sign_in.html', {'confirmation': _('Your account has been created, please go to your e-mail to confirm it.')})
        

def account_confirmation(request):
    if request.method == 'GET':
        try:
            context = services.expire_signin_token(request.GET.get('token'))
        except ObjectDoesNotExist as inst:
            return render(request, 'blog/registration/account_confirmation.html',  {'invalid_token': True})            

        return render(request, 'blog/registration/account_confirmation.html',  context) 

@login_required
def send_comment(request, post_url):
    if request.method == 'GET':
        return HttpResponseRedirect('/posts/{0}/'.format(post_url))
    try:
        services.send_comment(request.user, request.POST.get('comment-text'), Post.objects.get(url=post_url))
        return HttpResponseRedirect('/posts/{0}/#comment-tab'.format(post_url))
    except Exception as inst:
        print ('Error on saving comment information: {0}'.format(inst))
        return HttpResponse(500)    
        

@login_required
def send_answer_to_comment(request, post_url, comment_id):
    if request.method == 'GET':
        return HttpResponseRedirect('/posts/{0}/'.format(post_url))
    try:
        services.send_answer_to_comment(comment_id, request.user, request.POST.get('answer-text-{0}'.format(comment_id)), Post.objects.get(url=post_url))
        return HttpResponseRedirect('/posts/{0}/#comment-tab'.format(post_url))
    except Exception as inst:
        print ('Error on saving answer information: {0}'.format(inst))
        return HttpResponse(500)    
        
