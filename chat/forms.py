from typing import Any
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User,Profile

class UserUpdatedForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2','email']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

class Profileform(ModelForm):
    class Meta:
        model = Profile
        exclude = ['isonline','user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})