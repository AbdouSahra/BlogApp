from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from ckeditor.fields import RichTextField

LABEL_CHOICES = (
    ('E', 'economy'),
    ('P', 'politic'),
    ('S', 'sport'),
    ('T', 'tech'),
)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # content = models.TextField()
    content = RichTextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(upload_to='post/cover')
    category = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    likes = models.ManyToManyField(User, related_name='blogpost_like')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:detail", kwargs={
            'slug': self.slug
        })

    def delete(self, *args, **kwargs):
        self.post_image.delete()
        super().delete(*args, **kwargs)

    @property
    def comment_numbers(self):
        return Comment.objects.filter(post=self).count()

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

