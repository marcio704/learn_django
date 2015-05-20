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
	title = models.CharField(max_length=100)
	date = models.DateTimeField('date published')
	text = models.CharField(max_length=8000)
	resume = models.CharField(max_length=200)
	thumbnail = models.ImageField(upload_to='posts')
	category = models.ForeignKey(Category, blank=False, null=False)
	authors = models.ManyToManyField(Author, blank=False, null=False)


	def __str__(self):
		return "{0} - {1}".format(self.title, self.resume)

