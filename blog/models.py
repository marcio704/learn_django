from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/media/photos')


# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Author(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	personal_page = models.CharField(max_length=2000, blank=True, null=True)

	def __str__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=200)
	resume = models.CharField(max_length=200)
	text = models.CharField(max_length=8000)
	date = models.DateTimeField('date published')
	thumbnail = models.ImageField(upload_to='posts')
	category = models.ForeignKey(Category, blank=False, null=False)
	authors = models.ManyToManyField(Author, blank=False, null=False)


	def __str__(self):
		return "{0} - {1}".format(self.title, self.resume)

class User(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	photo = models.ImageField(upload_to='users', blank=True, null=True)
	creation_date = models.DateTimeField('date creation')
	blocked =  models.BooleanField(default=False)
	last_login = models.DateTimeField('date login')

	def __str__(self):
		return self.name

class Comment(models.Model):
	text = models.CharField(max_length=8000)
	date = models.DateTimeField('date creation')
	author = models.ForeignKey(User, blank=True, null=True)
	post = models.ForeignKey(Post, blank=True, null=True)
	answer_to = models.ForeignKey('self', blank=True, null=True)

	def __str__(self):
		return "{0} wrote: {1}".format(self.author.name, self.text)

class Contact(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	phone = models.CharField(max_length=25)
	message = models.CharField(max_length=8000)
	creation_date = models.DateTimeField('date creation')

	def __str__(self):
		return self.name

class AboutPage(models.Model):
	title = models.CharField(max_length=200)
	subtitle = models.CharField(max_length=100)
	text = models.CharField(max_length=8000)
	last_change = models.DateTimeField('date change')


	def __str__(self):
		return self.title

class ContactPage(models.Model):
	title = models.CharField(max_length=200)
	subtitle = models.CharField(max_length=100)
	text = models.CharField(max_length=8000)
	last_change = models.DateTimeField('date change')	

	def __str__(self):
		return self.title



