from django.db import models
from django.contrib.auth.models import User

class Typesofuser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    typeOfUser=models.CharField(max_length=299)

class QuestionBank(models.Model):
    question_id=models.IntegerField(primary_key=True)
    question=models.CharField(max_length=200)
    chapter=models.CharField(max_length=299,default=None)
    difficulty=models.CharField(max_length=200)
    marks=models.IntegerField()
    unit_no=models.IntegerField()
    subject=models.CharField(max_length=200)
    semester=models.IntegerField()
    year=models.IntegerField()
    subject_code=models.CharField(max_length=200)


class courses(models.Model):
    course_title=models.CharField(max_length=299)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)

class subCourses(models.Model):
    course_name=models.ForeignKey(courses,on_delete=models.CASCADE)
    chapters=models.CharField(max_length=299)
