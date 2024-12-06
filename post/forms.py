from django import forms

from user.models import Account
from .models import Post, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        }
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

image = forms.ImageField(required=True)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['bio']

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['avatar']