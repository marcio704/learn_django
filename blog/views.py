#from django.template import RequestContext, loader
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.contrib.auth import authenticate
from django.contrib.auth import  login as login_auth
from django.contrib.auth import logout as logout_auth
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from .models import Post
from .models import Category
from .models import Contact

from .models import UserProfile
from .models import Comment
from .utils import utils

from django.utils import timezone



import sys
import re

# Create your views here.

#TODO: Implement category list as a tag lib.
def index(request):
    post_list = Post.objects.all().order_by('-date')[:5]
    category_list_parts = utils.divideListByTwo(Category.objects.all())
    context = {'post_list': post_list, 'category_list_1': category_list_parts["list_1"], 'category_list_2': category_list_parts["list_2"]}
    
    return render(request, 'blog/index.html', context)

#TODO: Implement category list as a tag lib.
def detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    category_list_parts = utils.divideListByTwo(Category.objects.all())
    context = {'post': post, 'category_list_1': category_list_parts["list_1"], 'category_list_2': category_list_parts["list_2"]}

    return render(request, "blog/post/detail.html", context)
    
    
def all_posts(request):
    post_list = Post.objects.all()
    context = {'post_list': post_list}

    return render(request, 'blog/post/all_posts.html', context)

def posts_by_category(request, category_id):
    post_list = Post.objects.filter(category=category_id).order_by('-date')
    category = Category.objects.get(pk=category_id)
    context = {'post_list': post_list, 'category': category}

    return render(request, 'blog/post/posts_by_category.html', context)

def contact(request):
    return render(request, 'blog/contact.html')

def about(request):
    return render(request, 'blog/about.html')        

def send_contact(request):
    if request.method == 'POST':
        try:
            contact = Contact(name=request.POST.get('name'), email=request.POST.get('email'), phone=request.POST.get('phone'), message=request.POST.get('message'), creation_date=timezone.now())
            contact.save()
            return HttpResponse(200)
        except Exception as inst:
            print (type(inst))
            print (inst)
            print ('Error on saving contact information')
            
            return HttpResponse(500)    
    else:
        return HttpResponseRedirect('/contact')

def login(request):
    try:
        next = request.GET.get('next')
    except Exception as inst:
        print (type(inst))
        print ('On login process: {0}'.format(inst))        
    
    next = '/' if next is None else '/{0}/#comment-tab'.format(re.search(r'\d+', next).group(0)) 
    return render(request, 'blog/registration/login.html', {'next': next})  

def logout(request):
    logout_auth(request)
    return HttpResponseRedirect('/')

def auth(request):
    if request.method == 'POST':
        try: 
            user = authenticate(username=request.POST.get('login-username'), password=request.POST.get('login-password'))
            if user is not None:
                login_auth(request, user)
                return HttpResponseRedirect(request.POST.get('login-next'))  
            else:
                return render(request, 'blog/registration/login.html', {'validation': 'User/password not found!'})                    
        except Exception as inst:
            print (type(inst))
            print ('Error on authenticating user: {0}'.format(inst))
            
            return render(request, 'blog/registration/login.html')    
    else:
        return HttpResponseRedirect('/')

#TODO: build screen for sign in option (blog/registration/sign_in.html)
def sign_in(request):
    if request.method == 'POST':
        user = User.objects.create_user(username='john', email='jlennon@beatles.com', password='glassonion')
        user_profile = UserProfile.objects.create(user=user)
        print('User successfully saved!')
        return HttpResponseRedirect('/login')
    else:
        return render(request, 'blog/registration/sign_in.html')

@login_required
def send_comment(request, post_id):
    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user) 
            comment = Comment(text=request.POST.get('comment-text'), date=timezone.now(), author=user_profile, post=Post.objects.get(pk=post_id))
            comment.save()
            return HttpResponseRedirect('/{0}/#comment-tab'.format(post_id))
        except Exception as inst:
            print (type(inst))
            print (inst)
            print ('Error on saving comment information')
            
            return HttpResponse(500)    
    else:
        return HttpResponseRedirect('/{0}/'.format(post_id))

@login_required
def send_answer_to_comment(request, post_id, comment_id):
    if request.method == 'POST':
        try:
            answer_to = Comment.objects.get(pk=comment_id)
            user_profile = UserProfile.objects.get(user=request.user)
            comment = Comment(text=request.POST.get('answer-text-{0}'.format(comment_id)), date=timezone.now(), author=user_profile, post=Post.objects.get(pk=post_id), answer_to=answer_to)
            comment.save()
            return HttpResponseRedirect('/{0}/#comment-tab'.format(post_id))
        except Exception as inst:
            print (type(inst))
            print (inst)
            print ('Error on saving answer information')
            
            return HttpResponse(500)    
    else:
        return HttpResponseRedirect('/{0}/'.format(post_id))