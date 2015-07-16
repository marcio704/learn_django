import string
import json

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField
from blog.elastic import ElasticSearchClient
from blog.elastic import DocumentType

fs = FileSystemStorage(location='/media/photos')


# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class Author(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	personal_page = models.CharField(max_length=2000, blank=True, null=True)

	def __unicode__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=200)
	resume = models.CharField(max_length=200)
	text =RichTextField()
	date = models.DateTimeField('date published')
	thumbnail = models.ImageField(upload_to='posts')
	category = models.ForeignKey(Category, blank=False, null=False)
	authors = models.ManyToManyField(Author, blank=False, null=False)
	url = models.CharField(max_length=200, blank=False, null=False)

	def __unicode__(self):
		return self.title

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	photo = models.ImageField(upload_to='users', blank=True, null=True)

	def __unicode__(self):
		return self.user.first_name

class Comment(models.Model):
	text = models.CharField(max_length=8000)
	date = models.DateTimeField('date creation')
	author = models.ForeignKey(UserProfile, blank=True, null=True)
	post = models.ForeignKey(Post, blank=True, null=True)
	answer_to = models.ForeignKey('self', blank=True, null=True)

	def __unicode__(self):
		return self.text

class Contact(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	message = models.CharField(max_length=8000)
	creation_date = models.DateTimeField('date creation')
	is_email_sent = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

	def get_contact_email_message(self):
		return """
			From: {0}
			Email: {1}
			Date: {2}
			Message: {3}
		""".format(self.name, self.email, self.creation_date, self.message)

class TokenPassword(models.Model):
	user = models.ForeignKey(User)
	value = models.CharField(max_length=20)
	is_used = models.BooleanField(default=False)
	used_at = models.DateTimeField('date creation',blank=True, null=True)

class TokenUserSignIn(models.Model):
	user = models.ForeignKey(User)
	value = models.CharField(max_length=20)
	is_used = models.BooleanField(default=False)
	used_at = models.DateTimeField('date creation',blank=True, null=True)



def import_post_document(sender, instance, **kwargs):
	json_message = json.dumps({
		'id': 	 	"""{0}""".format(instance.id), 
		'title': 	"""{0}""".format(instance.title.decode('latin-1')),
	 	'resume':  	"""{0}""".format(instance.resume.encode('utf-8').decode('latin-1')), 
	 	'text':  	"""{0}""".format(instance.text.encode('utf-8').decode('latin-1'))
	 	})
	ElasticSearchClient().insert_document(instance.id, json_message, DocumentType.post)

# register the signal in order to import Post object/document to ElasticSearch
post_save.connect(import_post_document, sender=Post, dispatch_uid="search_import_elastic")
