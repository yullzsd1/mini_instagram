from django import forms
from .models import Account
from post.models import Comment


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['avatar']  # Поле только для аватара, чтобы обновить изображение

    def clean_avatar(self):
        # Валидация размера изображения
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Размер файла не должен превышать 5 МБ.")
        return avatar

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']