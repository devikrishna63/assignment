
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.index, name='home'),
    # Student
    path('student-login/', views.student_login, name='student_login'),
    path('student-register/', views.student_register, name='student_register'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student-assignments/', views.student_assignments, name='student_assignments'),
    path('submit/<int:id>/', views.submit_assignment, name='submit_assignment'),
    path('student-profile/', views.student_profile, name='student_profile'),
    # Teacher
    path('teacher-login/', views.teacher_login, name='teacher_login'),
    path('teacher-register/', views.teacher_register, name='teacher_register'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('upload-assignment/', views.upload_assignment, name='upload_assignment'),
    path('view-submissions/', views.view_submissions, name='view_submissions'),
    path('mark/<int:id>/', views.mark_submission, name='mark_submission'),
    path('teacher-assignments/', views.teacher_assignments, name='teacher_assignments'),
    path('teacher-profile/', views.teacher_profile, name='teacher_profile'),
    path('submission-summary/', views.submission_summary, name='submission_summary'),
    # Admin
    path('view-students/', views.view_students, name='view_students'),
    path('help/', views.help_page, name='help'),
    # Logout
    path('logout/', views.logout, name='logout'),

]

