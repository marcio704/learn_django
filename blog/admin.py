from django.contrib import admin
from .models import Post
from .models import Category
from .models import Author
from .models import User
from .models import Comment
from .models import AboutPage
from .models import ContactPage

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields = ['date', 'title', 'text', 'resume', 'thumbnail', 'category', 'authors']

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']

class AuthorAdmin(admin.ModelAdmin):
	fields = ['name', 'email', 'personal_page']

class UserAdmin(admin.ModelAdmin):
	fields = ['name', 'email', 'photo', 'creation_date', 'blocked', 'last_login']

class CommentAdmin(admin.ModelAdmin):
	fields = ['title', 'text', 'date', 'author', 'post']

class AboutPageAdmin(admin.ModelAdmin):
	fields = ['title', 'subtitle', 'text', 'last_change']

class ContactPageAdmin(admin.ModelAdmin):
	fields = ['title', 'subtitle', 'text', 'last_change']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(ContactPage, ContactPageAdmin)

