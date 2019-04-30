from django.contrib.auth.models import User
from django import forms
from .models import feedback
from django.contrib.auth.forms import UserCreationForm



class UserForm(forms.ModelForm):
    password = forms.CharField( widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']



class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def save(self,commit = True):
        user=super(RegistrationForm, self).save(commit = False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user


class FeedbackForm(forms.ModelForm):
    author = forms.CharField( label='',max_length=50 , widget=forms.TextInput(attrs={'class': "feed",'placeholder':"Ваше имя"}))
    number = forms.IntegerField( label='' , widget=forms.NumberInput(attrs={'class': "feed",'placeholder':"Ваш номер телефона"}))
    text = forms.CharField(label='', max_length=141 , widget=forms.Textarea(attrs={'class': "feed",'placeholder':"Ваше впечатление"}))
    class Meta:
        model = feedback
        fields = [ 'author', 'number','text']
    def save(self,commit = True):
        feed=super(FeedbackForm, self).save(commit = False)
        if commit:
            feed.save()
        return feed
