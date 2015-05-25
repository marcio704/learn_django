from django import template
from ..models import Comment


register = template.Library()


@register.simple_tag(takes_context=True)
def current_time(context, format_string):
    user = context['user']
    return user

@register.inclusion_tag('blog/post/comments.html')
def show_comments(post, user):
    comments = Comment.objects.filter(post=post, author=user)
    return {'comments': comments}    