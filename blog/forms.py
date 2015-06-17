from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'email', 'password',)
		labels = {
        	'username': _('Username'),
        	'first_name': _('Name'),
        	'email': _('Email'),
        	'password': _('Password'),
		}
	def is_valid(self):
		valid = super(UserForm, self).is_valid()
		if not valid:
			return valid

		user = None
		try:
			user = User.objects.get(username=self.cleaned_data['username'])
		except User.DoesNotExist:
			pass
		if user is not None:
			self._errors['username'] = _('This username is already in use, please choose another one')
			return False

		user_by_email = None
		try:
			user_by_email = User.objects.get(email=self.cleaned_data['email'])
		except User.DoesNotExist:
			pass
		if user_by_email is not None:
			self._errors['email'] = _('This e-mail is already in use, please choose another one')
			return False

		return True

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('photo',)