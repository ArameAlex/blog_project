from django.shortcuts import get_object_or_404
from django.http import Http404
from functools import wraps
from .models import Post_Model

def user_is_post_author(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        slug = kwargs['slug']
        post = get_object_or_404(Post_Model, slug=slug)
        if post.author == request.user:
            return function(request, *args, **kwargs)
        else:
            raise Http404("You are not authorized to perform this action.")
    return wrap
