from django import forms
from .models import Post_Model

class PostForm(forms.ModelForm):
    class Meta:
        model = Post_Model
        fields = ['title', 'short_content', 'content', 'post_tags']
