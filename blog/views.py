from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
#from django.template import RequestContext, loader
from .models import Post
from .models import Category
from django.views import generic
import math


# Create your views here.


"""
class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        # Return last 5 posts.
        return Post.objects.all()[:5]
"""
def index(request):
    post_list = Post.objects.all()[:5]
    category_list = Category.objects.all()
    half_size_ceil = int(math.ceil(len(category_list)/2))  
    half_size_floor = int(math.floor(len(category_list)/2))
    category_list_1 = category_list [:half_size_ceil]
    category_list_2 = category_list [len(category_list) - half_size_floor:]
    
    context = {'post_list': post_list, 'category_list_1': category_list_1, 'category_list_2': category_list_2}
    return render(request, 'blog/index.html', context)


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'        

def posts(request):
    post_list = Post.objects.all()
    context = {'post_list': post_list}

    return render(request, 'blog/all_posts.html', context)