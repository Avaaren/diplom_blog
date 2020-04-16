from django import forms
from .models import Comment, Post
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            ),
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            )
        }
class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'image', 'body', 'tags')