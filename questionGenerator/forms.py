from django import forms
from .models import Typesofuser,QuestionBank,courses,QuestionBank
from django.contrib.auth.models import User

class Registration(forms.Form):
    username=forms.CharField(max_length=299)
    password=forms.CharField(max_length=200,widget=forms.PasswordInput())


class TypesForm(forms.ModelForm):
    class Meta:
        fields='__all__'
        model=Typesofuser

class QuestionBankForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = QuestionBank

class UpdateUser(forms.ModelForm):
    class Meta:
        model=User
        fields=['username']

class coursesForm(forms.ModelForm):
    class Meta:
        model=courses
        fields=['course_title','user']

class UpdateQuestionForm(forms.ModelForm):
    class Meta:
        model=QuestionBank
        fields=['question']
