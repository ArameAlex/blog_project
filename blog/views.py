from django.shortcuts import render, get_object_or_404, redirect, Http404
from .models import Post_Model, Post_Tag
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import PostForm
from django.core.paginator import Paginator
from .permissions import user_is_post_author

def index(request):
    # get last 3 objects by date and render it
    posts = Post_Model.objects.all().order_by('-date')[0:3]
    return render(request, 'blog/index.html', {'posts': posts})

def posts(request):
    # get all posts order by date
    all_posts = Post_Model.objects.all().order_by('-date')
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/all-posts.html',  {'page_obj': page_obj})

def single_post(request, post_id):
    # get or 404 the name of post in the url
    post = get_object_or_404(Post_Model, slug=post_id)
    if request.method == 'POST':
        # if delete button pressed it would delete
        if 'delete_post' in request.POST:
            post.delete()
            return redirect('starting-page')
        # if update , go to the update page
        if 'update_post' in request.POST:
            return redirect('update-post', slug=post_id)
    return render(request, 'blog/post-detail.html', {'post': post})

def users(request):
    # get all the users order by id
    User = get_user_model()
    users = User.objects.all().order_by('-id')
    paginator = Paginator(users, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/user/all-users.html', {'users': page_obj})

def user_detail(request, user_id):
    # get the user by his name and filter the posts with his username
    User = get_user_model()
    users = get_object_or_404(User, username=user_id)
    user_model = Post_Model.objects.filter(author=users).order_by('-date')
    paginator = Paginator(user_model, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/user/user-detail.html', {'web_user': users, 'model': page_obj})

def tags(request):
    # show all the tags
    tags = Post_Tag.objects.all()
    paginator = Paginator(tags, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category/all-tags.html', {'tags': page_obj})

def posts_by_tag(request, tag):
    # filter the post by tags in url
    posts = Post_Model.objects.filter(post_tags__tag=tag)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category/posts_by_tag.html', {'posts': page_obj, 'tag': tag})

def sign_in(request):
    # if request was post get username - password
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        # authenticate username with name and password
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            # if username and password was correct login
            login(request, user)
            return redirect('starting-page')
        else:
            # else give an error massage and get back to page
            messages.error(request, 'Invalid username or password.')
            return redirect('sign-in')
    else:
        return render(request, 'blog/sign-in.html')

def sign_out(request):
    # log out
    logout(request)
    return redirect('starting-page')

def search(request):
    if request.method == 'POST':
        # get the requested search
        searched = request.POST['searched']
        # get all the all objects that contains search in title
        # with upper or lower case words
        search_post = Post_Model.objects.filter(Q(title__icontains=searched) | Q(content__icontains=searched))
        return render(request, 'blog/search.html', {'searched': searched, 'posts': search_post})
    else:
        # search should be a post method not get
        return render(request, 'blog/search.html')


@login_required
def create_post(request):
    if request.method == 'POST':
        # get the inserted title, shrt_cnt, content, list of the tags
        title = request.POST.get('title')
        short_content = request.POST.get('Shrt_Cnt')
        content = request.POST.get('content')
        post_tags = request.POST.getlist('post_tags')
        # get the author, the user that is logged in
        author = request.user
        # create a new object with that information
        post = Post_Model.objects.create(title=title, short_content=short_content,
                                         content=content, author=author,)
        # set the tags to selected tags
        post.post_tags.set(post_tags)
        return redirect('starting-page')
    else:
        # get the all tags to show the tags
        tags_create = Post_Tag.objects.all()
        return render(request, 'blog/create-post.html', {'tags': tags_create})

@login_required
@user_is_post_author
def update_post(request, slug):
    # get the post
    post = get_object_or_404(Post_Model, slug=slug)
    # if the request was post
    if request.method == 'POST':
        # get the value from 4 fields of the instance post and render it into html file
        form = PostForm(request.POST, instance=post)
        # if the post is valid save it and return to home page
        if form.is_valid():
            form.save()
            return redirect('starting-page')
    # if method was get, show the value of fields
    else:
        form = PostForm(instance=post)
    # it would return the html file
    return render(request, 'blog/update-post.html', {'form': form})

@login_required
def new_tag(request):
    if request.method == 'POST':
        post_tag = request.POST.get('tag-adder')
        new_tag = Post_Tag.objects.create(tag=post_tag)
        new_tag.save()
        return redirect('create-post')
    else:
        return render(request, 'blog/new-tag.html')
