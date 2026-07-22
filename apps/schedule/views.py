"""
Views for schedule app - timetable generation and resource management.
"""

import logging
import os

from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.conf import settings
from decouple import config

from .forms import (
    RoomForm,
    InstructorForm,
    MeetingTimeForm,
    CourseForm,
    DepartmentForm,
    BatchForm,
    SectionForm,
    SuggestionForm,
    PDFUploadForm,
)
from .models import (
    Room,
    Instructor,
    MeetingTime,
    Course,
    Department,
    Batch,
    Section,
    TimeTableModel,
    PDF,
)
from .services import TimetableGeneratorService

logger = logging.getLogger(__name__)


def _is_staff(user):
    return user.is_active and user.is_staff


# ============================================================================
# Public Pages
# ============================================================================


def index(request):
    """Homepage."""
    return render(request, "index_modern.html")


def aboutus(request):
    """About us page."""
    return render(request, "aboutus_modern.html")


def help(request):
    """Help page."""
    return render(request, "help_modern.html")


def terms(request):
    """Terms and conditions page."""
    return render(request, "terms_modern.html")


def index1(request):
    """Login page."""
    return render(request, "login_modern.html")


def about(request):
    """About page for viewer."""
    return render(request, "about.html")


# ============================================================================
# Admin Dashboard
# ============================================================================


@login_required
def admindash(request):
    """Admin dashboard."""
    return render(request, "admindashboard_modern.html")


def admin_login(request):
    """Admin login handler using Django's built-in authentication."""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, "login_modern.html")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                logger.info("User '%s' logged in successfully.", username)
                messages.success(request, "Login successful!")
                return redirect("schedule:admindash")
            else:
                logger.warning("Disabled user '%s' attempted login.", username)
                messages.error(request, "This account has been disabled.")
        else:
            logger.warning("Failed login attempt for username '%s'.", username)
            messages.error(request, "Invalid username or password.")

    return render(request, "login_modern.html")


@require_POST
def admin_logout(request):
    """Admin logout handler. Requires POST."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("schedule:index")


# ============================================================================
# Instructors/Teachers Management
# ============================================================================


@login_required
def addInstructor(request):
    """Add new instructor."""
    if request.method == "POST":
        form = InstructorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Instructor added successfully!")
            return redirect("schedule:addInstructors")
    else:
        form = InstructorForm()
    return render(request, "addInstructors_modern.html", {"form": form})


@login_required
def inst_list_view(request):
    """List all instructors."""
    instructors = Instructor.objects.all()
    return render(request, "inslist_modern.html", {"instructors": instructors})


@require_POST
@login_required
@user_passes_test(_is_staff)
def delete_instructor(request, pk):
    """Delete an instructor. Staff only."""
    inst = get_object_or_404(Instructor, pk=pk)
    inst.delete()
    messages.success(request, f"Instructor '{inst.name}' deleted.")
    return redirect("schedule:editinstructor")


# ============================================================================
# Rooms Management
# ============================================================================


@login_required
def addRooms(request):
    """Add new room."""
    form = RoomForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Room added successfully!")
        return redirect("schedule:addRooms")
    return render(request, "addRooms_modern.html", {"form": form})


@login_required
def room_list(request):
    """List all rooms."""
    rooms = Room.objects.all()
    return render(request, "roomslist_modern.html", {"rooms": rooms})


@require_POST
@login_required
@user_passes_test(_is_staff)
def delete_room(request, pk):
    """Delete a room. Staff only."""
    rm = get_object_or_404(Room, pk=pk)
    rm.delete()
    messages.success(request, f"Room '{rm.r_number}' deleted.")
    return redirect("schedule:editrooms")


# ============================================================================
# Meeting Times Management
# ============================================================================


@login_required
def addTimings(request):
    """Add new meeting time."""
    form = MeetingTimeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Meeting time added successfully!")
        return redirect("schedule:addTimings")
    return render(request, "addTimings_modern.html", {"form": form})


@login_required
def meeting_list_view(request):
    """List all meeting times."""
    meeting_times = MeetingTime.objects.all()
    return render(request, "mtlist_modern.html", {"meeting_times": meeting_times})


@require_POST
@login_required
@user_passes_test(_is_staff)
def delete_meeting_time(request, pk):
    """Delete a meeting time. Staff only."""
    mt = get_object_or_404(MeetingTime, pk=pk)
    mt.delete()
    messages.success(request, f"Meeting time '{mt}' deleted.")
    return redirect("schedule:editmeetingtime")


# ============================================================================
# Courses Management
# ============================================================================


@login_required
def addCourses(request):
    """Add new course."""
    form = CourseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Course added successfully!")
        return redirect("schedule:addCourses")
    return render(request, "addCourses_modern.html", {"form": form})


@login_required
def course_list_view(request):
    """List all courses."""
    courses = Course.objects.all()
    return render(request, "courseslist_modern.html", {"courses": courses})


@require_POST
@login_required
@user_passes_test(_is_staff)
def delete_course(request, pk):
    """Delete a course. Staff only."""
    crs = get_object_or_404(Course, pk=pk)
    crs.delete()
    messages.success(request, f"Course '{crs.course_name}' deleted.")
    return redirect("schedule:editcourse")


# ============================================================================
# Departments Management
# ============================================================================


@login_required
def addDepts(request):
    """Add new department."""
    form = DepartmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Department added successfully!")
        return redirect("schedule:addDepts")
    return render(request, "addDepts_modern.html", {"form": form})


@login_required
def department_list(request):
    """List all departments."""
    departments = Department.objects.all()
    return render(request, "deptlist_modern.html", {"departments": departments})


@require_POST
@login_required
@user_passes_test(_is_staff)
def delete_department(request, pk):
    """Delete a department. Staff only."""
    dept = get_object_or_404(Department, pk=pk)
    dept.delete()
    messages.success(request, f"Department '{dept.dept_name}' deleted.")
    return redirect("schedule:editdepartment")


# ============================================================================
# Batches Management
# ============================================================================


@login_required
def addBatches(request):
    """Add new batch."""
    form = BatchForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Batch added successfully!")
        return redirect("schedule:addBatches")
    return render(request, "addBatches_modern.html", {"form": form})


@login_required
def batch_list(request):
    """List all batches."""
    batches = Batch.objects.all()
    return render(request, "batchlist_modern.html", {"batches": batches})


@require_POST
@login_required
@user_passes_test(_is_staff)
def delete_batch(request, pk):
    """Delete a batch. Staff only."""
    batch = get_object_or_404(Batch, pk=pk)
    batch.delete()
    messages.success(request, f"Batch '{batch.batch_name}' deleted.")
    return redirect("schedule:editbatch")


# ============================================================================
# Sections Management
# ============================================================================


@login_required
def addSections(request):
    """Add new section."""
    form = SectionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Section added successfully!")
        return redirect("schedule:addSections")
    return render(request, "addSections_modern.html", {"form": form})


@login_required
def section_list(request):
    """List all sections."""
    sections = Section.objects.all()
    return render(request, "seclist_modern.html", {"sections": sections})


@require_POST
@login_required
@user_passes_test(_is_staff)
def delete_section(request, pk):
    """Delete a section. Staff only."""
    sec = get_object_or_404(Section, pk=pk)
    sec.delete()
    messages.success(request, f"Section '{sec.section_id}' deleted.")
    return redirect("schedule:editsection")


# ============================================================================
# Timetable Generation
# ============================================================================


@login_required
def generate(request):
    """Display timetable generation page."""
    return render(request, "generate_modern.html")


@require_POST
@login_required
@user_passes_test(_is_staff)
def timetable(request):
    """Generate timetable using genetic algorithm. Staff only."""
    try:
        schedule = TimetableGeneratorService.generate()
        sections = Section.objects.all()
        times = MeetingTime.objects.all()

        return render(
            request,
            "gentimetable_modern.html",
            {"schedule": schedule, "sections": sections, "times": times},
        )
    except Exception:
        logger.exception("Error generating timetable")
        messages.error(
            request,
            "An error occurred while generating the timetable. Please try again.",
        )
        return redirect("schedule:generate")


@login_required
def edittt(request):
    """Edit timetable page."""
    return render(request, "edittimetable.html")


# ============================================================================
# PDF Management
# ============================================================================


def pdf_list(request):
    """List all PDFs for viewer."""
    pdfs = PDF.objects.all()
    return render(request, "pdf_list.html", {"pdfs": pdfs})


@login_required
def lists(request):
    """List all PDFs for admin."""
    pdfs = PDF.objects.all()
    return render(request, "list_modern.html", {"pdfs": pdfs})


@login_required
def upload_pdf(request):
    """Upload a new PDF."""
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "PDF uploaded successfully!")
            return redirect("schedule:lists")
    else:
        form = PDFUploadForm()
    return render(request, "upload_pdf_modern.html", {"form": form})


def view_pdf(request, pk):
    """View a PDF."""
    pdf = get_object_or_404(PDF, pk=pk)
    return render(request, "view_pdf_modern.html", {"pdf": pdf})


@require_POST
@login_required
def delete_pdf(request, pk):
    """Delete a PDF."""
    pdf = get_object_or_404(PDF, pk=pk)
    pdf.delete()
    return redirect("schedule:lists")


@login_required
def download_pdf(request, pk):
    """Download a PDF file."""
    pdf = get_object_or_404(PDF, pk=pk)
    file_path = pdf.file.path
    if not os.path.exists(file_path):
        messages.error(request, "PDF file not found on server.")
        return redirect("schedule:lists")
    response = FileResponse(
        open(file_path, "rb"), as_attachment=True, filename=os.path.basename(file_path)
    )
    return response


# ============================================================================
# Suggestions
# ============================================================================


def suggestion_view(request):
    """Handle suggestion form."""
    if request.method == "POST":
        form = SuggestionForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            suggestion = form.cleaned_data["suggestion"]
            attachment = request.FILES.get("attachment")

            subject = f"Suggestion from {name}"
            body = f"Name: {name}\nEmail: {email}\nSuggestion:\n{suggestion}"

            contact_email = config("CONTACT_EMAIL", default="admin@example.com")
            mailto_link = f"mailto:{contact_email}?subject={subject}&body={body}"

            if attachment:
                mailto_link += f"&attachment={attachment.name}"

            return render(
                request, "suggestion_redirect.html", {"mailto_link": mailto_link}
            )
    else:
        form = SuggestionForm()

    return render(request, "suggestion_form.html", {"form": form})


def suggestion_thanks_view(request):
    """Thank you page for suggestions."""
    return render(request, "suggestion_thanks.html")


# ============================================================================
# Health Check
# ============================================================================


def health_check(request):
    """Health check endpoint for load balancers and monitoring."""
    import json
    from django.db import connection

    status = {"status": "ok"}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status["database"] = "ok"
    except Exception:
        status["database"] = "error"
        status["status"] = "degraded"

    http_status = 200 if status["status"] == "ok" else 503
    return HttpResponse(
        json.dumps(status),
        content_type="application/json",
        status=http_status,
    )
