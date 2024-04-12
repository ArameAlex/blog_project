from django.urls import path

from . import views

urlpatterns = [
    # post
    path('', views.index, name='starting-page'),
    path('blogs/', views.posts, name='posts-page'),
    path('blogs/<slug:post_id>', views.single_post, name='post-detail-page'),
    # users
    path('users', views.users, name='user-list'),
    path('users/<slug:user_id>', views.user_detail, name='user-detail'),
    # sign-in
    path('log_in', views.sign_in, name='sign-in'),
    path('log_out', views.sign_out, name='sign-out'),
    # categories
    path('categories', views.tags, name='all-tags'),
    path('categories/<str:tag>/', views.posts_by_tag, name='posts-by-tag'),
    # search
    path('search', views.search, name='search'),
    #create-update
    path('create', views.create_post, name='create-post'),
    path('blogs/update/<slug:slug>', views.update_post, name='update-post'),
    path('create/tag', views.new_tag, name='create-new-tag')
]
