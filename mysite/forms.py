from django import forms
from django.contrib.auth import get_user_model
from .models import Post,Comment,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title','text',)


class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('author', 'text',)


class UserCreateForm(UserCreationForm):
	class Meta:
		fields = ('username','email','password1','password2')
		model = get_user_model()

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['username'].label = "Display Name"
		self.fields["email"].label = "Email Address"

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date','avatar')