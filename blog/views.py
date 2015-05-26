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
from .utils import utils

from django.utils import timezone

from django.shortcuts import render_to_response
from django.template.context_processors import csrf

import sys

# Create your views here.

#TODO: Implement category list as a tag lib.
def index(request):
    post_list = Post.objects.all().order_by('-date')[:5]
    category_list_parts = utils.divideListByTwo(Category.objects.all())
    context = {'post_list': post_list, 'category_list_1': category_list_parts["list_1"], 'category_list_2': category_list_parts["list_2"]}
    
    return render(request, 'blog/index.html', context)

#TODO: Replace hard-coded author by logged user
#TODO: Implement category list as a tag lib.
def detail(request, post_id):
    user = User.objects.get(pk=3)
    post = Post.objects.get(pk=post_id)
    category_list_parts = utils.divideListByTwo(Category.objects.all())
    context = {'post': post, 'user': user, 'category_list_1': category_list_parts["list_1"], 'category_list_2': category_list_parts["list_2"]}


    context.update(csrf(request))

    return render_to_response("blog/post/detail.html", context)
    
    

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

#TODO: Replace hard-coded author by logged user
def send_comment(request, post_id):
    if request.method == 'POST':
        try: 
            comment = Comment(text=request.POST.get('comment-text'), date=timezone.now(), author=User.objects.get(pk=3), post=Post.objects.get(pk=post_id))
            comment.save()
            return HttpResponseRedirect('/{0}/#comment-tab'.format(post_id))
        except Exception as inst:
            print (type(inst))
            print (inst)
            print ('Error on saving comment information')
            
            return HttpResponse(500)    
    else:
        return HttpResponseRedirect('/')


def send_answer_to_comment(request, post_id, comment_id):
    if request.method == 'POST':
        try:
            answer_to = Comment.objects.get(pk=comment_id)

            comment = Comment(text=request.POST.get('answer-text-{0}'.format(comment_id)), date=timezone.now(), author=User.objects.get(pk=3), post=Post.objects.get(pk=post_id), answer_to=answer_to)
            comment.save()
            return HttpResponseRedirect('/{0}/#comment-tab'.format(post_id))
        except Exception as inst:
            print (type(inst))
            print (inst)
            print ('Error on saving answer information')
            
            return HttpResponse(500)    
    else:
        return HttpResponseRedirect('/{0}/'.format(post_id))