from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post_Tag(models.Model):
    tag = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.tag


class Post_Model(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='user_admin')
    date = models.DateField(auto_now=True)
    short_content = models.CharField(max_length=360, db_index=True)
    content = models.TextField()
    slug = models.SlugField(default="", null=False, blank=True, max_length=200, unique=True)
    post_tags = models.ManyToManyField(Post_Tag)

    def get_absolute_url(self):
        return reverse('post-detail-page', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
