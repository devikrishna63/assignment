from django.contrib import admin
from .models import Student, Teacher, Assignment, Submission
from django.contrib.auth.hashers import make_password
from django import forms

admin.site.site_header = "🎓 College Assignment Management Admin"
admin.site.site_title = "College Assignment Management"
admin.site.index_title = "Welcome to Admin Dashboard"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = None  

    list_display = (
        'regno',
        'name',
        'year',
        'department',
        'semester',
        'gender',
        'phone',
    )

    fields = (
        'regno',
        'name',
        'gender',
        'department',
        'year',
        'semester',
        'phone',
        'email',
        'address',
        'password',
    )

    search_fields = (
        'regno',
        'name',
        'department',
        'submissions__assignment__title',
        'submissions__assignment__teacher__name',
    )

    list_filter = ('department', 'year', 'semester', 'gender')
    ordering = ('regno',)

    def get_readonly_fields(self, request, obj=None):
        return ('regno',) if obj else ()

    def save_model(self, request, obj, form, change):
        if not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(obj.password)

        super().save_model(request, obj, form, change)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Only when adding new student
        if obj is None:
            if 'regno' in form.base_fields:
                form.base_fields['regno'].widget.attrs['autocomplete'] = 'off'

        return form

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = None  

    list_display = (
        'empid',
        'name',
        'gender',
        'email',
        'phone',
        'department',
    )

    fields = (
        'empid',
        'name',
        'gender',
        'department',
        'phone',
        'email',
        'address',
        'password',
    )

    search_fields = (
        'empid',
        'name',
        'department',
    )

    list_filter = ('department', 'gender')

    def get_readonly_fields(self, request, obj=None):
        return ('empid',) if obj else ()

    def save_model(self, request, obj, form, change):
        if not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(obj.password)

        super().save_model(request, obj, form, change)
        

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'teacher',
        'department',
        'year',
        'semester',
        'start_date',
        'end_date',
    )

    list_filter = (
        'department',
        'year',
        'semester',
        'start_date',
        'end_date',
    )

    search_fields = (
        'title',
        'teacher__name',
        'department',
    )

    ordering = ('year', 'semester', 'title')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'get_regno',
        'get_department',
        'get_year',
        'get_semester',
        'assignment',
        'marks',
        'status',
    )

    list_filter = (
        'status',
        'student__department',
        'assignment__year',
        'assignment__semester',
    )

    search_fields = (
        'student__name',
        'student__regno',
        'student__department',
        'assignment__title',
    )

    ordering = ('student__regno',)

    def get_regno(self, obj):
        return obj.student.regno
    get_regno.short_description = 'Reg No'

    def get_department(self, obj):
        return obj.student.department
    get_department.short_description = 'Department'

    def get_year(self, obj):
        return obj.student.year
    get_year.short_description = 'Year'

    def get_semester(self, obj):
        return obj.student.semester
    get_semester.short_description = 'Semester'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone
StudentAdmin.form = StudentForm
TeacherAdmin.form = TeacherForm