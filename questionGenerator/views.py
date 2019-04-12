from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,FileResponse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as lin, logout as lout
from .models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from xhtml2pdf import pisa
from django.template.loader import get_template
# import cStringIO as StringIO
from django.template import Context
from cgi import escape
from django.views.generic import View
from .utils import render_to_pdf
import nltk
from nltk.tokenize import word_tokenize
from django.core import mail
# from django.core.mail import EmailMessage,send_mail
from django.conf import settings
import smtplib

def register(request):
    if request.method=="POST":
        form=Registration(request.POST)
        if form.is_valid():
            name=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = User.objects.create_user(username=name,password=password)
            if user:
                lin(request,user)
                return redirect('complete',id=user.id)
            else:
                return redirect('index')
    else:
        form=Registration()
        context={
            'form':form
        }
        return render(request,'questionGenerator/index.html',context)

def complete(request,id):
    if request.method=="POST":
        form=TypesForm(request.POST)
        currentUser = request.user
        userr=User.objects.get(username=currentUser)
        # studentCheckbox = request.POST['student']
        # teacherCheckbox = request.POST['teacher']
        users=request.POST.get('user')
        ty=Typesofuser.objects.create(user_id=userr.id,typeOfUser=users)
        if users=="admin":
            ques=QuestionBank.objects.all()
            users=User.objects.all()
            form=coursesForm()
            subs=courses.objects.all()
            return render(request,'questionGenerator/admin.html',{'form':form,'ques':ques,'users':users,'subs':subs})
            lin(request,user)
        elif users=="teacher":
            return render(request,'questionGenerator/teacher.html')
            lin(request,user)
    else:
        user=User.objects.get(id=id)
        form=TypesForm()
        return render(request,'questionGenerator/complete.html',{'user':user,'form':form})


def login(request):
    if request.method=="POST":
        form=Registration(request.POST)
        if form.is_valid():
            name=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(username=name,password=password)
            if user:
                userr=User.objects.get(username=name)
                typ = Typesofuser.objects.get(user_id=userr.id)
                if typ.typeOfUser == "admin":
                    lin(request,user)
                    ques=QuestionBank.objects.all()
                    users=User.objects.all()
                    form=coursesForm()
                    subs=courses.objects.all()
                    return render(request,'questionGenerator/admin.html',{'form':form,'ques':ques,'users':users,'subs':subs})
                elif typ.typeOfUser == "teacher":
                    lin(request,user)
                    user=request.user
                    users=User.objects.get(username=user)
                    if courses.objects.filter(user_id=users.id).exists():
                        subs=courses.objects.get(user_id=users.id)
                        sub = subs.course_title
                        quest=QuestionBank.objects.filter(subject=sub)
                        print(sub)
                        return render(request,'questionGenerator/teacher.html',{'user':user,'quest':quest,'sub':sub})
                    else:
                        return render(request,'questionGenerator/teacher.html')
    else:
        form=Registration()
        return render(request,'questionGenerator/login.html',{'form':form})

@login_required(login_url='/login/')
def pages(request):
    return render(request,'questionGenerator/pages.html')

@login_required(login_url='/login/')
def addQuestion(request):
    if request.method=="POST":
        quest_id=request.POST['question_id']
        # print(quest_id)
        question=request.POST['question']
        # print(question)
        # marks=request.POST['marks']
        # print(marks)
        unit=request.POST['unit']
        chapter=request.POST['chapter']
        # print(unit)
        subject=request.POST['subject']
        # print(subject)
        semester=request.POST['semester']
        # print(semester)
        year=request.POST['year']
        # print(year)
        subject_code=request.POST['subject_code']
        # print(subject)
        easy=['What','Tell','List','Describe','Relate','Locate','Write','Find','State','Name','Comprehension','Explain','Interpret','Outline','Discuss','Distinguish','Predict','Restate','Translate','Compare','Describe']
        medium=['Solve','Show','Use','Illustrate','Construct','Complete','Examine','Classify','Analyse','Distinguish','Examine','Compare','Contrast','Investigate','Categorise','Identify','Explain','Separate','Advertise']
        hard=['Invent','Compose','Predict','Plan','Construct','Design','Imagine','Propose','Devise','Formulate','Select','Choose','Decide','Justify','Debate','Verify','Argue','Recommend','Assess','Discuss','Rate','Prioritise','Determine']
        newQuestions=word_tokenize(question)
        # print(newQuestions)
        # for i in newQuestions:
        #     if i in easy:
        #         print(newQuestions)
        #         print('.............................................................................')
        #         quest = QuestionBank.objects.create(chapter=chapter,marks=1,difficulty="Easy",question_id=quest_id,question=question,unit_no=unit,subject=subject,semester=semester,year=year,subject_code=subject_code)
        #     elif i in medium:
        #         quest = QuestionBank.objects.create(chapter=chapter,marks=5,difficulty="Medium",question_id=quest_id,question=question,unit_no=unit,subject=subject,semester=semester,year=year,subject_code=subject_code)
        #     elif i in hard:
        #         quest = QuestionBank.objects.create(chapter=chapter,marks=10,difficulty="Hard",question_id=quest_id,question=question,unit_no=unit,subject=subject,semester=semester,year=year,subject_code=subject_code)
        # # QuestionBank.objects.create(marks=100)
        # return HttpResponse('succesfully added')
        if newQuestions[0] in easy:
            QuestionBank.objects.create(chapter=chapter,marks=1,difficulty="Easy",question_id=quest_id,question=question,unit_no=unit,subject=subject,semester=semester,year=year,subject_code=subject_code)
        elif newQuestions[0] in medium:
            QuestionBank.objects.create(chapter=chapter,marks=5,difficulty="Medium",question_id=quest_id,question=question,unit_no=unit,subject=subject,semester=semester,year=year,subject_code=subject_code)
        elif newQuestions[0] in hard:
            QuestionBank.objects.create(chapter=chapter,marks=10,difficulty="Hard",question_id=quest_id,question=question,unit_no=unit,subject=subject,semester=semester,year=year,subject_code=subject_code)
        return HttpResponse("success")

@login_required(login_url='/login/')
def DisplayQuestion(request):
    questionBank=QuestionBank.objects.all()
    one = 1
    five=5
    ten=10
    return render(request,'questionGenerator/display.html',{'questionBank':questionBank,'one':one,'five':five,'ten':ten})



@login_required(login_url='/login/')
def some_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename="somefilename.pdf"

    buffer = BytesIO()

    p = canvas.Canvas(buffer)
    p.drawString(0,8.5*72, "Hello world")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def basee(request):
    return render(request,'questionGenerator/base.html')


def selector(request,id):
    if request.method=="POST":
        diffOne=request.POST['difficultyForA']
        diffTwo=request.POST['difficultyForB']
        diffThree=request.POST['difficultyForC']
        subject=request.POST['subject']
        chapter=request.POST['chapter']
        sem=request.POST['semester']
        year=request.POST['year']
        # amOne=request.POST['amountOne']
        # amTwo=request.POST['amountTwo']
        # amThree=request.POST['amountThree']
        questionBank=QuestionBank.objects.all()
        context={
        'diffOne':diffOne,
        'diffTwo':diffTwo,
        'diffThree':diffThree,
        'subject':subject,
        'sem':int(sem),
        'year':int(year),
        'questionBank':questionBank,
        'chapter':chapter
        }
        # questions=[]
        # yearr=[]
        # semm=[]
        # subjectt=[]
        # level=[]
        # for i in questionBank:
        #     yearr.append(i.year)
        #     semm.append(i.semester)
        #     subjectt.append(i.subject)
        #     level.append(i.difficulty)
        #
        # for j in questionBank:
        #     if year in yearr:
        #         if sem in semm:
        #             if subject in subjectt:
        #                 if diff in level:
        #                     questions.append(j.question)
        # print(questions)
        pdf = render_to_pdf('questionGenerator/questpaper.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        user=request.user
        users=User.objects.get(username=user)
        subs=courses.objects.get(user_id=users.id)
        sub = subs.course_title
        subCourse=subCourses.objects.filter(course_name_id=subs)
        chapters=subCourses.objects.get(id=id)
        return render(request,'questionGenerator/selector.html',{'sub':sub,'subCourse':subCourse,'chapters':chapters})
#
# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         questionBank=QuestionBank.objects.all()
#         context={
#         'questionBank':questionBank
#         }
#         pdf = render_to_pdf('questionGenerator/questpaper.html', context)
#         return HttpResponse(pdf, content_type='application/pdf')
#

# class GeneratePdf(View):
#     def get(self,request,*args,**kwargs):
#         template=get_template('questionGenerator/questpaper.html')
#         context={'a':a}
#         html=template.render(context)
#         pdf = render_to_pdf('questionGenerator/questpaper.html',context)
#         return HttpResponse(pdf,content_type='application/pdf')


def users(request,id):
    if request.method=="POST":
        user= User.objects.get(id=id)
        form=UpdateUser(data=request.POST,instance=user)
        update = form.save(commit=False)
        update.user = request.user
        update.save()
        return HttpResponse('Update Success')
    else:
        user = User.objects.get(id=id)
        form=UpdateUser()
        return render(request,'questionGenerator/specuser.html',{'form':form,'user':user})

def usersDelete(request,id):
    if request.method=="POST":
        user=User.objects.get(id=id).delete()

def AddCourse(request):
    if request.POST:
        form=coursesForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        else:
            return HttpResponse('adfaksjh')
    else:
        return render(request,'questionGenerator/admin.html')

def specific_questions(request,id):
    user=request.user
    users=User.objects.get(username=user)
    subs=courses.objects.get(user_id=users.id)
    sub = subs.course_title
    subCourses.objects.filter(course_name_id=subs)
    chapters=subCourses.objects.get(id=id)
    print(chapters.id)
    print('//...')
    print(subCourses.chapters)
    print(",.......")
    return render(request,'questionGenerator/questions.html',{'sub':sub,'subCourses':subCourses,'chapters':chapters,'subs':subs})

def addChapters(request):
    if request.method=="POST":
        chapName=request.POST['chapterName']
        user=request.user
        users=User.objects.get(username=user)
        subs=courses.objects.get(user_id=users.id)
        sub = subs.course_title
        chapters=subCourses.objects.create(course_name=subs,chapters=chapName)
        return redirect('addChapters')
    else:
        chapters=subCourses.objects.all()
        user=request.user
        users=User.objects.get(username=user)
        subs=courses.objects.get(user_id=users.id)
        if subCourses.objects.filter(course_name_id=subs).exists():
            subchapters=subCourses.objects.filter(course_name_id=subs)
            return render(request,'questionGenerator/addchapters.html',{'chapters':chapters,'subchapters':subchapters})
        else:
            print('nothing')
            return render(request,'questionGenerator/addchapters.html',{'chapters':chapters})

def allChapters(request):
    if request.method=="POST":
        diffOne=request.POST['difficultyForA']
        diffTwo=request.POST['difficultyForB']
        diffThree=request.POST['difficultyForC']
        subject=request.POST['subject']
        sem=request.POST['semester']
        year=request.POST['year']
        # amOne=request.POST['amountOne']
        # amTwo=request.POST['amountTwo']
        # amThree=request.POST['amountThree']
        questionBank=QuestionBank.objects.all()
        context={
        'diffOne':diffOne,
        'diffTwo':diffTwo,
        'diffThree':diffThree,
        'subject':subject,
        'sem':int(sem),
        'year':int(year),
        'questionBank':questionBank,
        }
        # questions=[]
        # yearr=[]
        # semm=[]
        # subjectt=[]
        # level=[]
        # for i in questionBank:
        #     yearr.append(i.year)
        #     semm.append(i.semester)
        #     subjectt.append(i.subject)
        #     level.append(i.difficulty)
        #
        # for j in questionBank:
        #     if year in yearr:
        #         if sem in semm:
        #             if subject in subjectt:
        #                 if diff in level:
        #                     questions.append(j.question)
        # print(questions)
        pdf = render_to_pdf('questionGenerator/formatforall.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
        # return render(request,'questionGenerator/login.html')
    else:
        user=request.user
        users=User.objects.get(username=user)
        subs=courses.objects.get(user_id=users.id)
        sub = subs.course_title
        subCourse=subCourses.objects.filter(course_name_id=subs)
        return render(request,'questionGenerator/allchapters.html',{'sub':sub})

# def sendmail(request):
#     server = smtplib.SMTP("smtp.gmail.com", 465)
#     server.connect("smtp.gmail.com",465)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()
#     server.login('rk.officialuser@gmail.com', "rkramanrk79")
#     text = msg.as_string()
#     server.sendmail('rk.officialuser@gmail.com', 'ramanronaldo79@gmail.com', "hi")
#     server.quit()

def usersCollection(request):
    user=User.objects.all()
    return render(request,'questionGenerator/users.html',{'user':user})

def UpdateQuestion(request,id):
    if request.method=="POST":
        quest=QuestionBank.objects.get(question_id=id)
        form=UpdateQuestionForm(data=request.POST,instance=quest)
        update = form.save(commit=False)
        update.save()
        return HttpResponse('Update Success')
    else:
        quest=QuestionBank.objects.get(question_id=id)
        form=UpdateQuestionForm()
        return render(request,'questionGenerator/updateQuestions.html',{'quest':quest,'form':form})

def DeleteQuestion(request,id):
    if request.method=="POST":
        quest=QuestionBank.objects.get(question_id=id).delete()

def logOut(request):
    # id = request.session["user_id"]
    use=request.user
    lout(request)
    return redirect('/')
