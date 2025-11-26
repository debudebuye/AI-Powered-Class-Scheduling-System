"""
Views for schedule app - timetable generation and resource management.
"""
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from decouple import config

from .forms import (
    RoomForm, InstructorForm, MeetingTimeForm, CourseForm,
    DepartmentForm, BatchForm, SectionForm, SuggestionForm, PDFUploadForm
)
from .models import (
    Room, Instructor, MeetingTime, Course, Department,
    Batch, Section, TimeTableModel, PDF
)
from .services import TimetableGeneratorService


# ============================================================================
# Public Pages
# ============================================================================

def index(request):
    """Homepage."""
    return render(request, 'index_modern.html')


def aboutus(request):
    """About us page."""
    return render(request, 'aboutus_modern.html')


def help(request):
    """Help page."""
    return render(request, 'help_modern.html')


def terms(request):
    """Terms and conditions page."""
    return render(request, 'terms_modern.html')


def index1(request):
    """Login page."""
    return render(request, 'login_modern.html')


def about(request):
    """About page for viewer."""
    return render(request, 'about.html')


# ============================================================================
# Admin Dashboard
# ============================================================================

@login_required
def admindash(request):
    """Admin dashboard."""
    return render(request, 'admindashboard_modern.html')


def admin_login(request):
    """Admin login handler."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        admin_username = config('ADMIN_USERNAME', default='admin')
        admin_password = config('ADMIN_PASSWORD', default='password')
        
        if username == admin_username and password == admin_password:
            messages.success(request, "Login successful!")
            return redirect('schedule:index1')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'adminlogin.html')


# ============================================================================
# Instructors/Teachers Management
# ============================================================================

@login_required
def addInstructor(request):
    """Add new instructor."""
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule:addInstructors')
    else:
        form = InstructorForm()
    return render(request, 'addInstructors.html', {'form': form})


@login_required
def inst_list_view(request):
    """List all instructors."""
    instructors = Instructor.objects.all()
    return render(request, 'inslist.html', {'instructors': instructors})


@login_required
def delete_instructor(request, pk):
    """Delete an instructor."""
    inst = get_object_or_404(Instructor, pk=pk)
    if request.method == 'POST':
        inst.delete()
        return redirect('schedule:editinstructor')


# ============================================================================
# Rooms Management
# ============================================================================

@login_required
def addRooms(request):
    """Add new room."""
    form = RoomForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('schedule:addRooms')
    return render(request, 'addRooms.html', {'form': form})


@login_required
def room_list(request):
    """List all rooms."""
    rooms = Room.objects.all()
    return render(request, 'roomslist.html', {'rooms': rooms})


@login_required
def delete_room(request, pk):
    """Delete a room."""
    rm = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        rm.delete()
        return redirect('schedule:editrooms')


# ============================================================================
# Meeting Times Management
# ============================================================================

@login_required
def addTimings(request):
    """Add new meeting time."""
    form = MeetingTimeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('schedule:addTimings')
    return render(request, 'addTimings.html', {'form': form})


@login_required
def meeting_list_view(request):
    """List all meeting times."""
    meeting_times = MeetingTime.objects.all()
    return render(request, 'mtlist.html', {'meeting_times': meeting_times})


@login_required
def delete_meeting_time(request, pk):
    """Delete a meeting time."""
    mt = get_object_or_404(MeetingTime, pk=pk)
    if request.method == 'POST':
        mt.delete()
        return redirect('schedule:editmeetingtime')


# ============================================================================
# Courses Management
# ============================================================================

@login_required
def addCourses(request):
    """Add new course."""
    form = CourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('schedule:addCourses')
    return render(request, 'addCourses.html', {'form': form})


@login_required
def course_list_view(request):
    """List all courses."""
    courses = Course.objects.all()
    return render(request, 'courseslist.html', {'courses': courses})


@login_required
def delete_course(request, pk):
    """Delete a course."""
    crs = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        crs.delete()
        return redirect('schedule:editcourse')


# ============================================================================
# Departments Management
# ============================================================================

@login_required
def addDepts(request):
    """Add new department."""
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('schedule:addDepts')
    return render(request, 'addDepts.html', {'form': form})


@login_required
def department_list(request):
    """List all departments."""
    departments = Department.objects.all()
    return render(request, 'deptlist.html', {'departments': departments})


@login_required
def delete_department(request, pk):
    """Delete a department."""
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        dept.delete()
        return redirect('schedule:editdepartment')


# ============================================================================
# Batches Management
# ============================================================================

@login_required
def addBatches(request):
    """Add new batch."""
    form = BatchForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('schedule:addBatches')
    return render(request, 'addBatches.html', {'form': form})


@login_required
def batch_list(request):
    """List all batches."""
    batches = Batch.objects.all()
    return render(request, 'batchlist.html', {'batches': batches})


@login_required
def delete_batch(request, pk):
    """Delete a batch."""
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        batch.delete()
        return redirect('schedule:editbatch')


# ============================================================================
# Sections Management
# ============================================================================

@login_required
def addSections(request):
    """Add new section."""
    form = SectionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('schedule:addSections')
    return render(request, 'addSections.html', {'form': form})


@login_required
def section_list(request):
    """List all sections."""
    sections = Section.objects.all()
    return render(request, 'seclist.html', {'sections': sections})


@login_required
def delete_section(request, pk):
    """Delete a section."""
    sec = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        sec.delete()
        return redirect('schedule:editsection')


# ============================================================================
# Timetable Generation
# ============================================================================

@login_required
def generate(request):
    """Display timetable generation page."""
    return render(request, 'generate.html')


@login_required
def timetable(request):
    """Generate timetable using genetic algorithm."""
    try:
        schedule = TimetableGeneratorService.generate()
        sections = Section.objects.all()
        times = MeetingTime.objects.all()
        
        return render(request, 'gentimetable.html', {
            'schedule': schedule,
            'sections': sections,
            'times': times
        })
    except Exception as e:
        messages.error(request, f"Error generating timetable: {str(e)}")
        return redirect('schedule:generate')


@login_required
def edittt(request):
    """Edit timetable page."""
    return render(request, 'edittimetable.html')


# ============================================================================
# PDF Management
# ============================================================================

def pdf_list(request):
    """List all PDFs for viewer."""
    pdfs = PDF.objects.all()
    return render(request, 'pdf_list.html', {'pdfs': pdfs})


@login_required
def lists(request):
    """List all PDFs for admin."""
    pdfs = PDF.objects.all()
    return render(request, 'list.html', {'pdfs': pdfs})


@login_required
def upload_pdf(request):
    """Upload a new PDF."""
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('schedule:lists')
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})


def view_pdf(request, pk):
    """View a PDF."""
    pdf = get_object_or_404(PDF, pk=pk)
    return render(request, 'view_pdf.html', {'pdf': pdf})


@require_POST
@login_required
def delete_pdf(request, pk):
    """Delete a PDF."""
    pdf = get_object_or_404(PDF, pk=pk)
    pdf.delete()
    return redirect('schedule:lists')


def download_pdf(request, pk):
    """Download a PDF file."""
    pdf = get_object_or_404(PDF, pk=pk)
    response = FileResponse(open(pdf.file.path, 'rb'), as_attachment=True)
    return response


# ============================================================================
# Suggestions
# ============================================================================

def suggestion_view(request):
    """Handle suggestion form."""
    if request.method == 'POST':
        form = SuggestionForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            suggestion = form.cleaned_data['suggestion']
            attachment = request.FILES.get('attachment')

            subject = f'Suggestion from {name}'
            body = f"Name: {name}\nEmail: {email}\nSuggestion:\n{suggestion}"
            mailto_link = f"mailto:debadeba015@gmail.com?subject={subject}&body={body}"

            if attachment:
                mailto_link += f"&attachment={attachment.name}"

            return render(request, 'suggestion_redirect.html', {'mailto_link': mailto_link})
    else:
        form = SuggestionForm()
    
    return render(request, 'suggestion_form.html', {'form': form})


def suggestion_thanks_view(request):
    """Thank you page for suggestions."""
    return render(request, 'suggestion_thanks.html')
