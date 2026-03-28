from django.shortcuts import render,redirect, get_object_or_404
from .models import Teacher
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from datetime import date
from django.http import HttpResponse
from .models import Student, Assignment, Submission
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
def index(request):
    return render(request,'index.html')
def admin_login(request):
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['password']

        user = authenticate(username=u, password=p)

        if user is not None and user.is_superuser:
            return redirect('/admin/')
        else:
            messages.error(request,"Invalid Admin Credentials")

    # return render('/admin/')
    return redirect('/admin/')

#
def student_register(request):

    if request.method == "POST":

        Student.objects.create(
            regno=request.POST['regno'],
            name=request.POST['name'],
            gender=request.POST['gender'],
            department=request.POST['department'],
            year=request.POST['year'],
            semester=request.POST['semester'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            address=request.POST.get('address',''),
            password = make_password(request.POST['password'])
        )

        messages.success(request, "Registration Successful. Please Login.")
        return redirect('/student-login/')

    return render(request,'student_register.html')
def student_login(request):

    if request.method=="POST":
        regno = request.POST['regno']
        password = request.POST['password']
        student = Student.objects.filter(regno=regno).first()

        if student and check_password(password, student.password):
            request.session['student'] = student.id
            return redirect('/student-dashboard/')
        else:
            return render(request,'student_login.html',{'error':'Invalid Login'})

    return render(request,'student_login.html')

def student_dashboard(request):

    if 'student' not in request.session:
        return redirect('/student-login')

    student = Student.objects.get(id=request.session['student'])

    return render(request,'student_dashboard.html',{
        'student': student
    })
def student_assignments(request):

    student_id = request.session.get('student')

    if not student_id:
        return redirect('student_login')

    student = Student.objects.get(id=student_id)

    assignments = Assignment.objects.filter(
        department=student.department,
        year=student.year,
        semester=student.semester
    )

    submitted = Submission.objects.filter(student=student)

    submitted_ids = submitted.values_list('assignment_id', flat=True)

    unsubmitted = assignments.exclude(id__in=submitted_ids)

    today = date.today()

    return render(request,'student_assignments.html',{
        'submitted': submitted,
        'unsubmitted': unsubmitted,
        'today': today,
        'student': student,
         'total': assignments.count(),
    })
def submit_assignment(request, id):

  
    student_id = request.session.get('student')

    if not student_id:
        return redirect('student_login')

    student = Student.objects.get(id=student_id)
    # assignment = Assignment.objects.get(id=id)
    assignment = get_object_or_404(Assignment, id=id)

    if Submission.objects.filter(student=student, assignment=assignment).exists():
        return HttpResponse("Already submitted")

    if assignment.end_date < date.today():
        return HttpResponse("Deadline over")

    if request.method == "POST":

        file = request.FILES.get('file')

        if not file:
            return HttpResponse("Please upload a file")

        Submission.objects.create(
            student=student,
            assignment=assignment,
            file=file,
            status="Submitted"
        )
        messages.success(request, "Assignment submitted successfully!")

        return redirect('/student-assignments/')

    return render(request, 'submit_assignment.html', {
        'assignment': assignment
    })
def student_profile(request):

    if 'student' not in request.session:
        return redirect('/student-login/')

    student = Student.objects.get(id=request.session['student'])

    edit = request.GET.get('edit')
    pwd = request.GET.get('pwd')
    success = request.GET.get('success')

    err = ''

    if request.method == "POST":

        
        if 'change_password' in request.POST:
            if not check_password(request.POST['oldpass'], student.password):
              err = "Old password wrong"

            elif request.POST['newpass'] != request.POST['confirmpass']:
             err = "Password mismatch"

            else:
             student.password = make_password(request.POST['newpass'])
             student.save()
             return redirect('/student-profile/?success=1')
        else:

            student.name = request.POST['name']
            student.gender = request.POST['gender']
            student.department = request.POST['department']
            student.year=request.POST['year']
            student.semester = request.POST['semester']
            student.phone = request.POST['phone']
            student.email = request.POST['email']
            student.address = request.POST.get('address', student.address)

            student.save()

            return redirect('/student-profile/?success=1')

    return render(request,'student_profile.html',{
        'student':student,
        'edit':edit,
        'pwd':pwd,
        'success':success,
        'err':err
    })

def teacher_login(request):
    if request.method == "POST":
        empid = request.POST['empid']
        password = request.POST['password']
        teacher = Teacher.objects.filter(empid=empid).first()

        if teacher and check_password(password, teacher.password):
            request.session['teacher'] = teacher.id
            request.session.modified = True
            return redirect('/teacher-dashboard/')
        else:
            return render(request, 'teacher_login.html', {
                'error': 'Invalid Employee ID or Password'
    })

    return render(request, 'teacher_login.html')
def teacher_register(request):

    if request.method == "POST":

        Teacher.objects.create(
            empid=request.POST['empid'],
            name=request.POST['name'],
            gender=request.POST['gender'],
            department=request.POST['department'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            address=request.POST.get('address',''),
            # password=request.POST['password']
            password = make_password(request.POST['password'])
        )

        return redirect('/teacher-login/')

    return render(request,'teacher_register.html')

def teacher_dashboard(request):

    if 'teacher' not in request.session:
        return redirect('/teacher-login')

    teacher = Teacher.objects.get(id=request.session['teacher'])

    return render(request,'teacher_dashboard.html',{
        'teacher': teacher
    })
def upload_assignment(request):

    if not request.session.get('teacher'):
        return redirect('/teacher-login')

    teacher = Teacher.objects.get(id=request.session['teacher'])

    if request.method == "POST":

        file = request.FILES.get('file')

        if file:  
            Assignment.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                file=file,
                teacher=teacher,
                department=request.POST['department'],
                year=request.POST['year'],
                semester=request.POST['semester'],
                start_date=request.POST['start_date'],
                end_date=request.POST['end_date']
            )
        else:   
            Assignment.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                teacher=teacher,
                department=request.POST['department'],
                year=request.POST['year'],
                semester=request.POST['semester'],
                start_date=request.POST['start_date'],
                end_date=request.POST['end_date']
            )

        messages.success(request, "Assignment uploaded successfully!")
        return redirect('upload_assignment')

    return render(request,'upload_assignment.html')
def view_submissions(request):

    if 'teacher' not in request.session:
        return redirect('/teacher-login/')

    teacher = get_object_or_404(Teacher, id=request.session['teacher'])

    year = request.GET.get('year')
    subject = request.GET.get('subject')
    department = request.GET.get('department')   # ✅ ADD

    # 🔹 Get assignments of this teacher
    assignments = Assignment.objects.filter(teacher=teacher)

    if department:   # ✅ ADD
        assignments = assignments.filter(department=department)

    if year:
        assignments = assignments.filter(year=year)

    if subject:
        assignments = assignments.filter(title__icontains=subject)

    # 🔹 Get relevant students
    students = Student.objects.filter(
        department__in=assignments.values_list('department', flat=True),
        year__in=assignments.values_list('year', flat=True),
        semester__in=assignments.values_list('semester', flat=True),
    ).distinct()

    total_students = students.count()

    # 🔹 All submissions
    submitted = Submission.objects.filter(
        assignment__in=assignments,
        student__in=students
    )

    # 🔹 Checked & Unchecked
    checked = submitted.filter(status="Checked").order_by('student__regno')
    unchecked = submitted.filter(status="Submitted").order_by('student__regno')

    total_checked = checked.count()
    total_unchecked = unchecked.count()

    # 🔹 Subject list
    subjects = Assignment.objects.filter(
        teacher=teacher
    ).values_list('title', flat=True).distinct()

    # 🔹 Department list (for dropdown)
    departments = Assignment.objects.filter(
        teacher=teacher
    ).values_list('department', flat=True).distinct()

    return render(request, 'view_submissions.html', {
        'checked': checked,
        'unchecked': unchecked,
        'selected_year': year,
        'subjects': subjects,
        'selected_subject': subject,
        'selected_department': department,   
        'departments': departments,          
        'total_students': total_students,
        'total_checked': total_checked,
        'total_unchecked': total_unchecked,
    })
def view_students(request):

    if 'teacher' not in request.session:
        return redirect('/teacher-login')

    teacher = Teacher.objects.get(id=request.session['teacher'])

    year = request.GET.get('year')

    students = Student.objects.filter(
        department=teacher.department
    )
    if year:
        students = students.filter(year=year)

    students = students.order_by('regno')

    total_students = students.count()

    return render(request,'view_students.html',{
        'students': students,
        'selected_year': year,
        'total_students': total_students
    })

def teacher_assignments(request):

    if 'teacher' not in request.session:
        return redirect('/teacher-login')

    teacher = Teacher.objects.get(id=request.session['teacher'])

    assignments = Assignment.objects.filter(teacher=teacher)

    return render(request,'teacher_assignments.html',{
        'assignments': assignments
    })


def teacher_profile(request):

    if 'teacher' not in request.session:
        return redirect('/teacher-login/')

    teacher = Teacher.objects.get(id=request.session['teacher'])

    edit = request.GET.get('edit')
    pwd = request.GET.get('pwd')
    success = request.GET.get('success')

    err = ''

    if request.method == "POST":

        
        if 'change_password' in request.POST:
            if not check_password(request.POST['oldpass'], teacher.password):
              err = "Old password wrong"

            elif request.POST['newpass'] != request.POST['confirmpass']:
             err = "Password mismatch"

            else:
              teacher.password = make_password(request.POST['newpass'])
              teacher.save()
              return redirect('/teacher-profile/?success=1')

        else:

            teacher.name = request.POST['name']
            teacher.gender = request.POST['gender']
            teacher.department = request.POST['department']
            teacher.phone = request.POST['phone']
            teacher.email = request.POST['email']
            teacher.address = request.POST.get('address', teacher.address)

            teacher.save()

            return redirect('/teacher-profile/?success=1')

    return render(request,'teacher_profile.html',{
        'teacher':teacher,
        'edit':edit,
        'pwd':pwd,
        'success':success,
        'err':err
    })

def mark_submission(request, id):

    if 'teacher' not in request.session:
        return redirect('/teacher-login/')

    teacher = Teacher.objects.get(id=request.session['teacher'])

    sub = get_object_or_404(
        Submission,
        id=id,
        assignment__teacher=teacher
    )

    if request.method == "POST":
        sub.marks = int(request.POST.get('marks'))
        sub.remarks = request.POST.get('remarks')
        sub.status = "Checked"   
        sub.save()
        return redirect('/view-submissions/')

    return render(request, 'mark.html', {'sub': sub})
def logout(request):
    request.session.flush()
    return redirect('/')
def submission_summary(request):

    if 'teacher' not in request.session:
        return redirect('/teacher-login/')

    teacher = Teacher.objects.get(id=request.session['teacher'])

    year = request.GET.get('year')
    semester = request.GET.get('semester')
    subject = request.GET.get('subject')
    department = request.GET.get('department')   # 🔥 ADD

    # 🔹 Assignments by teacher
    assignments = Assignment.objects.filter(teacher=teacher)

    if department:   # 🔥 ADD
        assignments = assignments.filter(department=department)

    if year:
        assignments = assignments.filter(year=year)

    if semester:
        assignments = assignments.filter(semester=semester)

    if subject:
        assignments = assignments.filter(title__icontains=subject)

    # 🔹 Students
    students = Student.objects.filter(
        department__in=assignments.values_list('department', flat=True),
        year__in=assignments.values_list('year', flat=True),
        semester__in=assignments.values_list('semester', flat=True),
    ).distinct().order_by('regno')

    total_students = students.count()

    # 🔹 Submitted
    submitted = Submission.objects.filter(
        assignment__in=assignments,
        student__in=students
    )

    total_submitted = submitted.count()

    # 🔹 Unsubmitted
    submitted_pairs = set(
        submitted.values_list('student_id', 'assignment_id')
    )

    unsubmitted = []

    for student in students:
        for assignment in assignments:
            if (student.id, assignment.id) not in submitted_pairs:
                unsubmitted.append({
                    'student': student,
                    'assignment': assignment
                })

    total_unsubmitted = len(unsubmitted)

    subjects = Assignment.objects.filter(teacher=teacher)\
        .values_list('title', flat=True).distinct()

    # 🔥 Department list for dropdown
    departments = Assignment.objects.filter(teacher=teacher)\
        .values_list('department', flat=True).distinct()

    return render(request, 'submission_summary.html', {
        'submitted': submitted,
        'unsubmitted': unsubmitted,
        'selected_year': year,
        'selected_semester': semester,
        'subjects': subjects,
        'selected_subject': subject,
        'selected_department': department,   # 🔥 ADD
        'departments': departments,          # 🔥 ADD
        'total_students': total_students,
        'total_submitted': total_submitted,
        'total_unsubmitted': total_unsubmitted
    })
def help_page(request):
    return render(request, 'help.html')