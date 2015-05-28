from django.contrib import admin
from .models import Post
from .models import Category
from .models import Author
from .models import UserProfile
from .models import Comment


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields = ['date', 'title', 'text', 'resume', 'thumbnail', 'category', 'authors']

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']

class AuthorAdmin(admin.ModelAdmin):
	fields = ['name', 'email', 'personal_page']

class UserProfileAdmin(admin.ModelAdmin):
	fields = ['user', 'photo']

class CommentAdmin(admin.ModelAdmin):
	fields = ['text', 'date', 'author', 'post', 'answer_to']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comment, CommentAdmin)

