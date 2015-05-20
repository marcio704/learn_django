from django.contrib import admin
from .models import Post
from .models import Category
from .models import Author

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields = ['date', 'title', 'text', 'resume', 'thumbnail', 'category', 'authors']

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']

class AuthorAdmin(admin.ModelAdmin):
	fields = ['name', 'email', 'personal_page']

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)