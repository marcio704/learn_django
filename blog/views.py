from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
#from django.template import RequestContext, loader
from .models import Post
from .models import Category
from django.views import generic


# Create your views here.


"""
def index(request):
	speech_list = Post.objects.all()
	context = {'speech_list': speech_list}
	return render(request, 'index.html', context)
"""
class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        """Return last 5 posts."""
        return Post.objects.all()[:5]


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'        