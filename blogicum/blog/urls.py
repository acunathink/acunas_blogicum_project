# from django.contrib.auth import get_user_model
from django.urls import path
# from django.views.generic import DetailView

from . import views

app_name = 'blog'

# User = get_user_model()

urlpatterns = [
    path('',
         views.PostListView.as_view(),
         name='index'),

    path('posts/create_post/',
         views.PostCreateView.as_view(),
         name='create_post'),

    path('posts/<int:pk>/',
         views.PostDetailView.as_view(),
         name='post_detail'),

    path('posts/<int:pk>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'),

    path('posts/<int:pk>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),

    path('profile/<slug:username>/',
         views.UserDetailView.as_view(),
         name='profile'),

    path('profile/<int:pk>/edit/',
         views.UserUpdateView.as_view(),
         name='edit_profile'),

    path('category/<slug:category_slug>/',
         views.CategoryDetailView.as_view(),
         name='category_posts'),

    path('<int:pk>/comment/',
         views.edit_comment,
         name='add_comment'),

    path('posts/<int:pk>/edit_comment/<int:comment_id>',
         views.CommentEdit.as_view(),
         name='edit_comment'),

    path('posts/<int:pk>/delete_comment/<int:comment_id>',
         views.CommentDelete.as_view(),
         name='delete_comment'),
]
