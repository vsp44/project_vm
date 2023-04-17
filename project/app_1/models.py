# from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(
        max_length=254, verbose_name='Email', unique=True
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to='profile/',
        blank=True,
        null=True,
    )
    phone = models.CharField('Телефон', max_length=25)
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    vip = models.CharField(max_length=4, blank=True, default='0', verbose_name='Vip')


class Post(models.Model):
    name = models.CharField(max_length=50, default='Название не указано', verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    likes = models.ManyToManyField(User, related_name='blogpost_like', verbose_name='Лайк')
    dislikes = models.ManyToManyField(User, related_name='blogpost_dislikes', verbose_name='Дизлайк')
    images = models.ImageField(
        'Картинка',
        upload_to='postimages/',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def number_of_likes(self):
        return self.likes.count()

    def number_of_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.text

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(
        "date published",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text



    # like = models.BooleanField(null=True, default=0)
    # avatar = models.ImageField(
    #     'Аватар',
    #     upload_to='profile/',
    #     blank=True,
    #     null=True,
    # )



# class Favorite(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, verbose_name='Пользователь'
#     )
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name='favorites',
#         verbose_name='Пост'
#     )
#     created = models.DateTimeField('дата публикации', auto_now_add=True)

#     class Meta:
#         verbose_name = 'Избранное'
#         verbose_name_plural = 'Избранное'
#         ordering = ('-created',)
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'post'], name='user_post'
#             )
#         ]

    # def __str__(self):
    #     return f'{self.post} в избранном у {self.user}'


# class Profile(models.Model):
#     user = models.OneToOneField(
#         User,
#         verbose_name='Пользователь',
#         related_name='profile',
#         on_delete=models.CASCADE
#     )
#     avatar = models.ImageField(
#         'Аватар',
#         upload_to='profile/',
#         blank=True,
#         null=True,
#     )
#     email_two = models.EmailField('Доп. емейл')
#     phone = models.CharField('Телефон', max_length=25)
#     first_name = models.CharField('Имя', max_length=50)
#     last_name = models.CharField(
#         'Фамилия',
#         max_length=50,
#         blank=True,
#         null=True,
#     )
#     slug = models.SlugField('URL', max_length=50)
#     # TODO: Адрес

#     def __str__(self):
#         return self.first_name

#     def get_absolute_url(self):
#         return reverse("profile", kwargs={"pk": self.user.pk})

#     class Meta:
#         verbose_name = 'Профиль'
#         verbose_name_plural = 'Профиля'


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):

#     if created:
#         Profile.objects.create(user=instance)



# @receiver
# def create_user_profile(sender, instance, **kwargs):

#     instance.profile.save()
