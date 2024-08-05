from django import forms
from .models import Blog,Sample
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm



class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        # filed = "__all__"
        # filed = ["title","content"]
        exclude = ["fk_user","is_published"]

class RegisterationForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','email','password1','password2')


class SampleFrom(forms.ModelForm):
    class Meta:
      model = Sample
      fields = "__all__"
        



