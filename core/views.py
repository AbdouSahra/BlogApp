from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count


class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    paginate_by = 6
    ordering = ['-date_created']

    """ def get_queryset(self): # ordering on highest likes
        queryset = super().get_queryset()
        queryset = queryset.annotate(number_of_likes=Count('likes')).order_by('-number_of_likes')
        return queryset"""


""" class CategoryView(ListView):
    model = Post
    template_name = 'category.html'
    slug_field = 'category'

    def get_context_data(self, *args, **kwargs):
        data = super(CategoryView, self).get_context_data(*args, **kwargs)
        post_catg = get_object_or_404(Post, category=self.kwargs['slug'])
        category_posts = Post.objects.filter(category=post_catg)
        data['category_posts'] = category_posts

        return data"""


def CategoryView(request, catg):
    category_posts = Post.objects.filter(category=catg)

    return render(request, 'category.html', {'catg': catg, 'category_posts': category_posts})


def BlogPostLikes(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('core:detail', args=[post.slug]))


class PostDetailView(DetailView):
    model = Post
    template_name = 'detail.html'
    #context_object_name = 'post'
    #form_class = CommentForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        post_comments = Comment.objects.filter(post=self.get_object()).order_by('-date_added')
        data['comments'] = post_comments
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)

        likes_connected = get_object_or_404(Post, slug=self.kwargs['slug'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True

        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked

        return data

    def post(self, request, slug, *args, **kwargs):
        new_comment = Comment(comment=request.POST.get('comment'),
                                name=self.request.user,
                                post=self.get_object())
        new_comment.save()
        return redirect('core:detail', slug=slug)


# def Detail(request, slug):
#    post = Post.objects.get(slug=slug)

#    if request.method == 'POST':
#        form = CommentForm(request.POST)
#            comment = form.save(commit=False)
#            comment.post = post
#            comment.save()
#        return redirect('core:detail', slug=post.slug)
#        form = CommentForm()
#
#    context = {
#        'post': post,
#        'form': form
#    }
#    return render(request, 'detail.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create.html'
    fields = ['title', 'slug', 'content', 'category', 'post_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'content', 'category', 'post_image']
    template_name = 'update.html'

    def get_context_data(self, **kwargs):
        data = super(PostUpdateView, self).get_context_data(**kwargs)
        data['update_form'] = data.get('form')
        return data

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('core:detail', args=[self.object.post.slug])

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.name:
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
