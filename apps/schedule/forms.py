from django.forms import ModelForm
from django import forms
from .models import (
    Room, Instructor, MeetingTime, Course, Department,
    Batch, Section, PDF
)

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['r_number', 'seating_capacity']
        widgets = {
            'r_number': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Auto-generated (e.g., R001) - Leave blank for auto ID'
            }),
            'seating_capacity': forms.NumberInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter seating capacity',
                'min': '1'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['r_number'].required = False
        self.fields['r_number'].help_text = "Leave blank to auto-generate (R001, R002, etc.)"


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['uid', 'name']
        widgets = {
            'uid': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Auto-generated (e.g., I001) - Leave blank for auto ID'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter instructor name'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uid'].required = False
        self.fields['uid'].help_text = "Leave blank to auto-generate (I001, I002, etc.)"

    def clean_uid(self):
        uid = self.cleaned_data.get('uid')
        if uid and Instructor.objects.filter(uid=uid).exists():
            if not self.instance.pk or self.instance.uid != uid:
                raise forms.ValidationError("This ID is already in use.")
        return uid
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Instructor.objects.filter(name=name).exists():
            if not self.instance.pk or self.instance.name != name:
                raise forms.ValidationError("This name is already in use.")
        return name

class MeetingTimeForm(ModelForm):
    class Meta:
        model = MeetingTime
        fields = ['pid', 'time', 'day']
        widgets = {
            'pid': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Auto-generated (e.g., MT01) - Leave blank for auto ID'
            }),
            'time': forms.Select(attrs={
                'class': 'form-control-modern'
            }),
            'day': forms.Select(attrs={
                'class': 'form-control-modern'
            }),
        }
        labels = {
            "pid": "Meeting Time ID",
            "time": "Time Slot",
            "day": "Day of the Week"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pid'].required = False
        self.fields['pid'].help_text = "Leave blank to auto-generate (MT01, MT02, etc.)"


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'course_name', 'max_numb_students', 'instructors']
        widgets = {
            'course_number': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Auto-generated (e.g., C001) - Leave blank for auto ID'
            }),
            'course_name': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter course name'
            }),
            'max_numb_students': forms.NumberInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Maximum number of students',
                'min': '1'
            }),
            'instructors': forms.SelectMultiple(attrs={
                'class': 'form-control-modern',
                'size': '4'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course_number'].required = False
        self.fields['course_number'].help_text = "Leave blank to auto-generate (C001, C002, etc.)"


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name']
        widgets = {
            'dept_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; display: inline-block; margin-left:10px;'
            }),
        }


class BatchForm(ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_id', 'batch_name', 'number_of_students', 'department', 'courses']
        widgets = {
            'batch_id': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Auto-generated (e.g., B001) - Leave blank for auto ID'
            }),
            'batch_name': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter batch name'
            }),
            'number_of_students': forms.NumberInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Number of students in batch',
                'min': '1'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control-modern'
            }),
            'courses': forms.SelectMultiple(attrs={
                'class': 'form-control-modern',
                'size': '4'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['batch_id'].required = False
        self.fields['batch_id'].help_text = "Leave blank to auto-generate (B001, B002, etc.)"


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['section_id', 'batch', 'num_class_in_week']
        widgets = {
            'section_id': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Auto-generated (e.g., S001) - Leave blank for auto ID'
            }),
            'batch': forms.Select(attrs={
                'class': 'form-control-modern'
            }),
            'num_class_in_week': forms.NumberInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Number of classes per week',
                'min': '1',
                'max': '7'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['section_id'].required = False
        self.fields['section_id'].help_text = "Leave blank to auto-generate (S001, S002, etc.)"
        
        
class SuggestionForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    suggestion = forms.CharField(widget=forms.Textarea)
    attachment = forms.FileField(required=False)


class PDFUploadForm(forms.ModelForm):
    ALLOWED_EXTENSIONS = ['.pdf']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    class Meta:
        model = PDF
        fields = ['title', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            import os
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                raise forms.ValidationError(
                    f"Only PDF files are allowed. Got: {ext}"
                )
            if file.size > self.MAX_FILE_SIZE:
                raise forms.ValidationError(
                    f"File size must be under {self.MAX_FILE_SIZE // (1024 * 1024)}MB."
                )
        return file
