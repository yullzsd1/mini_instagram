from django.conf import settings
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post',
        verbose_name='Автор поста'
    )
    content = models.TextField()
    image = models.ImageField(upload_to='posts_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Сортируем комментарии по дате (новые комментарии выше)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'post')  # Один пользователь может поставить лайк только одному посту

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.id}"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)

# Create your models here.
