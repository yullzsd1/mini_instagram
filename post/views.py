import json

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, View
from .models import Post, Comment, Like
from user.models import Account, AccountFollower
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from .forms import ProfileForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required

@login_required
def profile(request, user_id):
    user_profile = get_object_or_404(Account, id=user_id)
    is_following = AccountFollower.objects.filter(follower=request.user, following=user_profile).exists()

    context = {
        'user_profile': user_profile,
        'is_following': is_following,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    user_account = request.user  # Получаем текущего пользователя

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_account)
        if form.is_valid():
            form.save()  # Сохраняем обновленный профиль
            return redirect(reverse('profile-url', args=[user_account.id]))  # Перенаправляем на профиль
    else:
        form = ProfileForm(instance=user_account)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            # Проверяем, загружено ли изображение
            if not form.cleaned_data['image']:
                form.add_error('image',
                               'Пожалуйста, загрузите изображение.')  # Добавляем ошибку, если изображение не загружено
            else:
                post = form.save(commit=False)
                post.user = request.user  # Присваиваем автору поста текущего пользователя
                post.save()
                return redirect('home-url')  # Перенаправляем на главную страницу или на страницу постов
        else:
            # Если форма не валидна, просто перерисовываем форму с ошибками
            return render(request, 'create.html', {'form': form})
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

    class ProfileView(TemplateView):
        template_name = 'profile.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = kwargs.get('user_id')  # Получаем user_id из URL
        user_profile = get_object_or_404(Account, id=user_id)

        # Получаем все посты пользователя
        posts = Post.objects.filter(user=user_profile)
        context['user_profile'] = user_profile
        context['posts'] = posts
        return context



class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])  # Убедитесь, что это работает
        comment_text = request.POST.get('comment_text')  # Получаем текст комментария

        if comment_text:  # Если текст есть
            Comment.objects.create(
                content=comment_text,
                post=post,
                user=request.user
            )

        return redirect('home-url')
class LikeView(View):
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)

        # Если пользователь уже поставил лайк, удаляем его
        if Like.objects.filter(post=post, user=request.user).exists():
            Like.objects.filter(post=post, user=request.user).delete()
        else:
            # Если лайк не поставлен, ставим лайк
            Like.objects.create(post=post, user=request.user)

        # Перенаправляем обратно на страницу
        return redirect('home-url')


class ReelsView(TemplateView):
    template_name = 'reels.html'

class MessagesView(TemplateView):
    template_name = 'messages.html'



