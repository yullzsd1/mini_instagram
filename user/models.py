from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from post.models import Post
from user.managers import AccountManager


class Account(AbstractUser):
    """Модель для аккаунта"""

    username = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(4)],
        unique=True,
        db_index=True, # добавляет индекс для данной таблицы, чтобы делать поиск по имейлу быстрее)
        )
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True, # Это поле может быть пустым как на уровне базы данных)
        blank=True, # Этот параметр указывает, что поле может быть оставлено пустым в формах Django)
    )

    bio = models.TextField(null=True, blank=True, verbose_name='Описание')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    class Meta:
        verbose_name_plural = 'Аккаунты'
        verbose_name = 'Аккаунт'

    def get_context_data(self, **kwargs):
        posts = Post.objects.all()  # Получаем все посты

        for post in posts:
            post.likes_count = post.likes.filter(is_liked=True).count()  # Количество лайков
            post.comments_count = post.comments.count()  # Количество комментариев

            # Добавляем информацию о том, поставил ли текущий пользователь лайк
            post.is_liked_by_user = post.likes.filter(user=self.request.user, is_liked=True).exists()

        context = {
            'posts': posts,
        }

        return context


class AccountFollower(models.Model):
    following = models.ForeignKey(
        Account,
        verbose_name='на кого подписался',
        on_delete=models.CASCADE,
        related_name='my_followers',
    )

    follower = models.ForeignKey(
        Account,
        verbose_name='кто подписался',
        on_delete=models.CASCADE,
        related_name='my_following',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('following', 'follower')  # Ограничиваем, чтобы один и тот же пользователь не мог подписываться дважды
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'