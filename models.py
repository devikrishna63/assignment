
from django.db import models
from django.core.exceptions import ValidationError
import os

DEPARTMENT_CHOICES = [
    ('Tamil','Tamil'),
    ('English','English'),
    ('Commerce','Commerce'),
    ('History','History'),
    ('Economics','Economics'),
    ('Computer Science','Computer Science'),
    ('Maths','Maths'),
    ('Physics','Physics'),
    ('Chemistry','Chemistry'),
    ('Zoology','Zoology'),
    ('Botany','Botany'),
    ('BCA','BCA'),
]

YEAR_CHOICES = [
    (1,'First Year'),
    (2,'Second Year'),
    (3,'Third Year'),
]

SEMESTER_CHOICES = [
    ('Semester 1','Semester 1'),
    ('Semester 2','Semester 2'),
    ('Semester 3','Semester 3'),
    ('Semester 4','Semester 4'),
    ('Semester 5','Semester 5'),
    ('Semester 6','Semester 6'),
]
GENDER_CHOICES=[
    ('Male', 'Male'),
    ('Female', 'Female'),
]
class Student(models.Model):

    regno = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES
    )

    year = models.IntegerField(
        choices=YEAR_CHOICES
    )

    semester = models.CharField(
        max_length=20,
        choices=SEMESTER_CHOICES
    )

    phone = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField(blank=True)
    password = models.CharField(max_length=150)
    def clean(self):
        if not self.phone.isdigit() or len(self.phone) != 10:
            raise ValidationError({'phone': 'Phone number must be exactly 10 digits.'})
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name'] 

class Teacher(models.Model):
    empid = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField(blank=True)
    password = models.CharField(max_length=150)
    department = models.CharField(
    max_length=50,
    choices=DEPARTMENT_CHOICES
    )
    def clean(self):
        if not self.phone.isdigit() or len(self.phone) != 10:
            raise ValidationError({'phone': 'Phone number must be exactly 10 digits.'})

    def __str__(self):
        return self.name

class Assignment(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES
    )

    year = models.IntegerField(
        choices=YEAR_CHOICES
    )

    semester = models.CharField(
        max_length=20,
        choices=SEMESTER_CHOICES
    )

    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

class Submission(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    marks = models.PositiveIntegerField(null=True,blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(
    max_length=20,
    choices=[
        ('Submitted', 'Submitted'),
        ('Checked', 'Checked')
    ],
    default='Submitted'
    
    )
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.student.name
    class Meta:
        unique_together = ['student', 'assignment']

    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)
