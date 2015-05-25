#from django.template import RequestContext, loader
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Post
from .models import Category
from .models import Contact
from .models import AboutPage
from .models import ContactPage
from .models import User
from .models import Comment

from datetime import datetime

import math
import sys


# Create your views here.

def index(request):
    post_list = Post.objects.all().order_by('-date')[:5]
    category_list_parts = divideListByTwo(Category.objects.all())
    context = {'post_list': post_list, 'category_list_1': category_list_parts["list_1"], 'category_list_2': category_list_parts["list_2"]}
    
    return render(request, 'blog/index.html', context)

#TODO: Replace hard-coded author by logged user
def detail(request, post_id):
    user = User.objects.get(pk=3)
    post = Post.objects.get(pk=post_id)
    category_list_parts = divideListByTwo(Category.objects.all())
    context = {'post': post, 'user': user, 'category_list_1': category_list_parts["list_1"], 'category_list_2': category_list_parts["list_2"]}
    
    return render(request, 'blog/post/detail.html', context)

def posts(request):
    post_list = Post.objects.all()
    context = {'post_list': post_list}

    return render(request, 'blog/post/all_posts.html', context)

def contact(request):
    contact_page = ContactPage.objects.all()[0]
    context = {'contact_page': contact_page}

    return render(request, 'blog/contact.html', context)

def about(request):
    about = AboutPage.objects.all()[0]
    context = {'about': about}

    return render(request, 'blog/about.html', context)        

def send_contact(request):
    if request.method == 'POST':
        try:
            contact = Contact(name=request.POST.get('name'), email=request.POST.get('email'), phone=request.POST.get('phone'), message=request.POST.get('message'), creation_date=datetime.now())
            contact.save()
            return HttpResponse(200)
        except Exception as inst:
            print (type(inst))
            print (inst)
            print ('Error on saving contact information')
            
            return HttpResponse(500)    
    else:
        return HttpResponseRedirect('/contact')

#TODO: Replace hard-coded author by logged user
def send_comment(request, post_id):
    if request.method == 'POST':
        try:
            comment = Comment(text=request.POST.get('text'), date=datetime.now(), author=User.objects.get(pk=3), post=Post.objects.get(pk=post_id))
            comment.save()
            return HttpResponse(200)
        except Exception as inst:
            print (type(inst))
            print (inst)
            print ('Error on saving comment information')
            
            return HttpResponse(500)    
    else:
        return HttpResponseRedirect('/')

#Utils
def divideListByTwo (whole_list):
    half_size_ceil = int(math.ceil(len(whole_list)/2))  
    half_size_floor = int(math.floor(len(whole_list)/2))
    list_1 = whole_list [:half_size_ceil]
    list_2 = whole_list [len(whole_list) - half_size_floor:]

    return {"list_1": list_1, "list_2": list_2}

