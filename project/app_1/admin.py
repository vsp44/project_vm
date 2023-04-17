from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ['pk', 'name', 'text', 'author', 'pub_date']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['pk', 'username', 'avatar', 'email', 'first_name', 'last_name']

# @admin.register(Post.likes)
# class PostAdmin(admin.ModelAdmin):

#     list_display = ['pk_meta']

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['pk', 'avatar', 'email_two', 'phone', 'first_name', 'last_name']

    # def get_html_photo(self, object):
    #     if object.avatar:
    #         return mark_safe(f"<img src='{object.avatar}' width=50>")
    #     else:
    #         return "Нет фото"

    # get_html_photo.short_description = "Миниатюра"
