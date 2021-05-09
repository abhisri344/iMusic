from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Album,Song
User = get_user_model()


class Mylogin(forms.Form):
    UserName=forms.CharField(max_length=100)
    Password=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        u=self.cleaned_data['UserName']
        p=self.cleaned_data['Password']
        v=authenticate(username=u,password=p)
        if v is None:
            raise forms.ValidationError('UserName or Password did not match') 
class Register(forms.ModelForm):
    Password=forms.CharField(widget=forms.PasswordInput)
    Re_Password=forms.CharField(widget=forms.PasswordInput)        
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
    def clean(self):
        data=super(Register,self).clean() 
        p=data['Password'] 
        p1=data['Re_Password']  
        if p!=p1:
            raise forms.ValidationError('Password\'s did not match')

class Addalbum(forms.ModelForm):
     class Meta:
        model=Album
        fields=['title','artist','genre','year','image']
                
# class Addsong(forms.ModelForm):
#      class Meta:
#         model=Song
#         fields=['al_id','title','artist','genre','sfile','image']                