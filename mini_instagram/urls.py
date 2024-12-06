# mini_instagram/urls.py

from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from user.views import follow_user, unfollow_user, search_users
from post import views
from user.views import UserRegistrationView, LoginPageView, UserMakeLoginView, UserMakeRegistrationView, HomeView, \
    UploadAvatarView
from post.views import ProfileView, ReelsView, MessagesView, LikeView, AddCommentView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', UserRegistrationView.as_view(), name='registration-url'),
    path('login/', LoginPageView.as_view(), name='login-url'),
    path('make-login/', UserMakeLoginView.as_view(), name='make-login-url'),
    path('home/', HomeView.as_view(), name='home-url'),
    path('make-registration/', UserMakeRegistrationView.as_view(), name='make-registration-url'),
    path('profile/', ProfileView.as_view(), name='profile-url'), 
    path('reels/', ReelsView.as_view(), name='reels-url'),
    path('messages/', MessagesView.as_view(), name='messages-url'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    path('upload-avatar/<int:user_id>/', UploadAvatarView.as_view(), name='upload_avatar'),
    path('like/<int:post_id>/', LikeView.as_view(), name='like-url'),
    path('search/', search_users, name='search-users-url'),  # Поиск пользователей
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile-url'),  
    path('create/', views.create_post, name='create-post'),

    path('post/<int:pk>/add_comment/', AddCommentView.as_view(), name='add-comment'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)