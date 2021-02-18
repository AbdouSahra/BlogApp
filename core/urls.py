from django.urls import path
from .views import (PostListView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    PostDetailView,
                    BlogPostLikes,
                    CommentDeleteView,
                    CategoryView)

app_name = 'core'

urlpatterns = [
    path('', PostListView.as_view(), name="home"),
    # path('article/<slug>', PostDetailView.as_view(), name="detail"),
    path('article/<slug>', PostDetailView.as_view(), name="detail"),
    path('create/', PostCreateView.as_view(), name="create"),
    path('article/<slug>/update', PostUpdateView.as_view(), name="update"),
    path('article/<slug>/delete', PostDeleteView.as_view(), name="delete"),
    path('blogpost-like/<slug>', BlogPostLikes, name='like'),
    path('article/<slug>/delete', PostDeleteView.as_view(), name="delete"),
    path('comment/<int:pk>', CommentDeleteView.as_view(), name="dltz"),
    path('category/<str:catg>', CategoryView, name="category"),
]
