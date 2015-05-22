from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=200)
	email = forms.CharField(label='Email', max_length=200)
	phone = forms.CharField(label='Phone', max_length=25)
	message = forms.CharField(label='Message', max_length=8000)
	creation_date = forms.DateTimeField(label='Date')
