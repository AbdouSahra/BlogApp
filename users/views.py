from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from core.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.info(request, f'You Can Login {username}')
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/settings.html'
    form_class = UserUpdateForm
    success_url = '/'

    def get_object(self):
        return self.request.user


class ProfileDetail(DetailView):
    model = Profile
    template_name = 'users/profile.html'
    slug_field = "user__username"

    def get_context_data(self, *args, **kwargs):
        data = super(ProfileDetail, self).get_context_data(*args, **kwargs)
        page_user= get_object_or_404(Profile, user__username=self.kwargs['slug'])
        data['page_user'] = page_user

        users_post = get_object_or_404(User, username=self.kwargs['slug'])
        posts = Post.objects.filter(author=users_post).order_by('-date_created')
        data['posts'] = posts

        return data


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'users/edit.html'
    slug_field = "user__username"
    fields = ['picture', 'bio']

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])

    def test_func(self):
        profile = self.get_object()

        if self.request.user == profile.user:
            return True
        else:
            return False
