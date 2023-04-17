"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

from app_1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", PostView.as_view(), name="index"),
    path("vip/<int:pk>", VipView.as_view(), name='vip'),
    path("addpage", PostCreateView.as_view(), name="add_page"),
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(template_name='logged_out.html'),name='logout'),
    path('login/', LoginView.as_view(template_name='login.html', success_url = reverse_lazy('index')), name='login'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post_detail'),
    path('blogpost-like/<int:pk>', BlogPostLike, name="blogpost_like"),
    path('blogpost-dislikes/<int:pk>', BlogPostdislikes, name="blogpost_dislikes"),
    path('posts/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('deletecom/<int:comment_id>', remove_comment, name='remove_comment'),
    path('calc/', home, name='calc')
    # path('user_profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
    # path('create_profile_page/',CreateProfilePageView.as_view(), name='create_user_profile'),
    # Отложеные
    # path('author/<int:pk>', AuthorView.as_view(), name='author'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
