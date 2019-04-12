from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.register,name='register'),
    path('complete/<int:id>/',views.complete,name='complete'),
    path('login/',views.login,name='login'),
    path('pages/',views.pages,name='pages'),
    path('questions/',views.addQuestion,name='addQuestion'),
    path('display/',views.DisplayQuestion,name="DisplayQuestion"),
    path('some/',views.some_view),
    path('',views.basee),
    path('select/<int:id>/',views.selector,name='selector'),
    path('users/<int:id>/',views.users,name='users'),
    path('add_courses/',views.AddCourse,name="addcourse"),
    path('specific_questions/<int:id>/',views.specific_questions,name="specific_questions"),
    path('add_chapters/',views.addChapters,name="addChapters"),
    path('allChapters/',views.allChapters,name='allChapters'),
    path('users/',views.usersCollection,name="userCollection"),
    path('update_questions/<int:id>/',views.UpdateQuestion,name='UpdateQuestion'),
    path('delete_questions/<int:id>/',views.DeleteQuestion,name='DeleteQuestion'),
    path('delete_users/<int:id>/',views.usersDelete,name='usersDelete'),
    path('logout/',views.logOut,name="logOut")
    # path('send_mail/',views.sendmail,name='sendmail')
    # path('down/',views.GeneratePdf.as_view(),name='downn')
]
