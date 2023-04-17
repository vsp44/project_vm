from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.utils.decorators import method_decorator
from django.urls import reverse

from project.settings import BASE_DIR


from .forms import *
from .Test4 import f
from .models import *

# Create your views here.

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class PostView(ListView):
    model = Post
    print(BASE_DIR)

    # def like(self, request, username):
    #     user = get_object_or_404(User, username=username)
    #     # post_list = user.posts.all()
    #     if request.user.is_authenticated:
    #         following = Favorite.objects.filter(
    #             user=request.user, author=user
    #         ).exists()
    #     else:
    #         following = False
    #     context = {
    #         # 'author': user,
    #         # 'posts': post_list,
    #         # 'page_obj': paginator(post_list, request),
    #         'following': following,
    #     }
    #     return render(request, 'app_1/post_list.html', context)

# def postdete


# class PostDetailView(DetailView):
#     model = Post

class BlogPostDetailView(DetailView):
    model = Post
    # template_name = 'BlogPost_detail.html'
    # context_object_name = 'object'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # print(kwargs.pk)
        connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        disliked = False
        if connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        if connected.dislikes.filter(id=self.request.user.id).exists():
            disliked = True
        data['number_of_likes'] = connected.number_of_likes()
        data['post_is_liked'] = liked
        data['number_of_dislikes'] = connected.number_of_dislikes()
        data['post_is_dislikes'] = disliked
        data['form'] = CommentForm() # добавляем форму в контекст
        comments = connected.comments.all()
        data['comments'] = comments
        return data

def BlogPostLike(request, pk):
    print(BASE_DIR)
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)

    return HttpResponseRedirect(f'/post/{pk}/')

def BlogPostdislikes(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)

    return HttpResponseRedirect(f'/post/{pk}/')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form1 = CommentForm(request.POST or None)
    if form1.is_valid():
        comment = form1.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('post_detail', pk=post_id) # заменил post_id на pk так как у 'post_detail' нет именованного аргумента post_id

@login_required
def remove_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('post_detail', pk=comment.post.id)

#     def like(request, username):
#         user = get_object_or_404(User, username=username)
#         # post_list = user.posts.all()
#         if request.user.is_authenticated:
#             following = Favorite.objects.filter(
#                 user=request.user, author=user
#             ).exists()
#         else:
#             following = False
#         context = {
#             # 'author': user,
#             # 'posts': post_list,
#             # 'page_obj': paginator(post_list, request),
#             'following': following,
#         }
#         return render(request, 'app_1/post_detail.html', context)

# class AddPageView(LoginRequiredMixin, CreateView):
#     form_class = AddPostForm
#     template_name = 'add_page.html'
#     model = Post
#     success_url = reverse_lazy('index')

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return dict(list(context.items()))

class PostCreateView(CreateView):
    # form_class = PostCreateForm
    template_name = 'app_1/create_post.html'
    model = Post
    form_class = AddPostForm
    # fields = ['name', 'text']
    success_url = reverse_lazy('index')
    # model = Profile
    """Добавление автора к посту"""
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author_id = self.request.user.id
        self.object.save()
        return super().form_valid(form)

    """Проверка на анонима"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('index')
    # model = Profile

    """Проверка на автора"""
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        if request.user != post.author:
            #  return HttpResponse('Вы не можете удалить этот пост!')
            return render(request, 'delete.html')
        return super().dispatch(request, *args, **kwargs)

class PostUpdateView(UpdateView):
    model = Post
    fields = ['name', 'text']
    success_url = reverse_lazy('index')
    # model = Profile
    """Проверка на автора"""
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        if request.user != post.author:
            #  return HttpResponse('Вы не можете изменить этот пост!')
            return render(request, 'update.html')
        return super().dispatch(request, *args, **kwargs)

class SignUp(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'
    # model = Profile

# class LoginUser(LoginView):
#     form_class = LoginUserForm
#     template_name = 'login.html'

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Авторизация")
#         return dict(list(context.items()) + list(c_def.items()))

#     def get_success_url(self):
#         return reverse_lazy('index')


# def logout_user(request):
#     logout(request)
#     return redirect('index')


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    form_class = ProfileForm
    model = User
    success_url = reverse_lazy('index')


class VipView(LoginRequiredMixin, UpdateView):
    template_name = 'vip.html'
    form_class = VipForm
    model = User
    success_url = reverse_lazy('index')

# class calc(TemplateView):
#     template_name = 'calc.html'

#     def cl(self, num1, sign, num2):
#         return eval(f"{num1}{sign}{num2}")

def Addition(num1,num2):
    result = int(num1) + int(num2)
    if result < 0:
        result = f'{result} (минус {f(str(abs(int(result))))})'
    else:
        result = f'{result} ({f(str(abs(int(result))))})'
    return result

def Subtract(num1,num2):
    result = int(num1) - int(num2)
    if result < 0:
        result = f'{result} (минус {f(str(abs(int(result))))})'
    else:
        result = f'{result} ({f(str(abs(int(result))))})'
    return result

def Divide(num1,num2):
    result = int(num1) / int(num2)
    if result < 0:
        result = f'{result} (минус {f(str(abs(int(result))))})'
    else:
        result = f'{result} ({f(str(abs(int(result))))})'
    return result

def Multiply(num1,num2):
    result = int(num1) * int(num2)
    if result < 0:
        result = f'{result} (минус {f(str(abs(int(result))))})'
    else:
        result = f'{result} ({f(str(abs(int(result))))})'
    return result

def home(request):
    if request.method == 'POST':
        num1 = request.POST['num1']
        num2 = request.POST['num2']
        if 'add' in request.POST:
            result = Addition(num1,num2)
            return render(request,'calc.html',{'result':result})

        if 'sub' in request.POST:
            result = Subtract(num1,num2)
            return render(request,'calc.html',{'result':result})

        if 'div' in request.POST:
            result = Divide(num1,num2)
            return render(request,'calc.html',{'result':result})

        if 'mul' in request.POST:
            result = Multiply(num1,num2)
            return render(request,'calc.html',{'result':result})
    return render(request,'calc.html')

# def postdetail(request, username):
#     user = get_object_or_404(User)
#     post_list = user.posts.all()
#     if request.user.is_authenticated:
#         following = Favorite.objects.filter(
#             user=request.user, author=user
#         ).exists()
#     else:
#         following = False
#     context = {
#         # 'author': user,
#         # 'posts': post_list,
#         # 'page_obj': paginator(post_list, request),
#         'following': following,
#         'Post': Post
#     }
#     return render(request, 'posts/profile.html', context)

# from django.views.generic.detail import DetailView
# class ShowProfilePageView(DetailView):
#     model = Profile
#     template_name = 'user_profile.html'

#     def get_context_data(self, *args, **kwargs):
#         users = Profile.objects.all()
#         context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
#         page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
#         context['page_user'] = page_user
#         return context


# class CreateProfilePageView(CreateView):
#     model = Profile

#     template_name = 'create_profile.html'
#     fields = ['profile_pic', 'bio', 'facebook', 'twitter', 'instagram']
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

#     success_url = reverse_lazy('user_profile')

# Отложеные

# class AuthorView(DetailView):
#     template_name = 'author.html'
#     model = User
#     model = Post
#     # model = Profile
