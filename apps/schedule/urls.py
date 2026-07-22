"""
URL configuration for schedule app.
"""

from django.urls import path
from . import views

app_name = "schedule"

urlpatterns = [
    # Public pages
    path("", views.index, name="index"),
    path("about/", views.aboutus, name="aboutus"),
    path("help/", views.help, name="help"),
    path("terms/", views.terms, name="terms"),
    # Admin
    path("admin-dashboard/", views.admindash, name="admindash"),
    path("manage/", views.admin_login, name="adminlogin"),
    path("logout/", views.admin_logout, name="logout"),
    # Teachers/Instructors
    path("teachers/add/", views.addInstructor, name="addInstructors"),
    path("teachers/", views.inst_list_view, name="editinstructor"),
    path("teachers/<int:pk>/delete/", views.delete_instructor, name="deleteinstructor"),
    # Rooms
    path("rooms/add/", views.addRooms, name="addRooms"),
    path("rooms/", views.room_list, name="editrooms"),
    path("rooms/<int:pk>/delete/", views.delete_room, name="deleteroom"),
    # Timings
    path("timings/add/", views.addTimings, name="addTimings"),
    path("timings/", views.meeting_list_view, name="editmeetingtime"),
    path(
        "timings/<str:pk>/delete/", views.delete_meeting_time, name="deletemeetingtime"
    ),
    # Courses
    path("courses/add/", views.addCourses, name="addCourses"),
    path("courses/", views.course_list_view, name="editcourse"),
    path("courses/<str:pk>/delete/", views.delete_course, name="deletecourse"),
    # Departments
    path("departments/add/", views.addDepts, name="addDepts"),
    path("departments/", views.department_list, name="editdepartment"),
    path(
        "departments/<int:pk>/delete/", views.delete_department, name="deletedepartment"
    ),
    # Batches
    path("batches/add/", views.addBatches, name="addBatches"),
    path("batches/", views.batch_list, name="editbatch"),
    path("batches/<int:pk>/delete/", views.delete_batch, name="deletebatch"),
    # Sections
    path("sections/add/", views.addSections, name="addSections"),
    path("sections/", views.section_list, name="editsection"),
    path("sections/<str:pk>/delete/", views.delete_section, name="deletesection"),
    # Timetable generation
    path("timetable/generate/", views.generate, name="generate"),
    path("timetable/create/", views.timetable, name="timetable"),
    path("timetable/edit/", views.edittt, name="edit_tt"),
    # PDF Management
    path("pdfs/", views.lists, name="lists"),
    path("pdfs/upload/", views.upload_pdf, name="upload_pdf"),
    path("pdfs/<int:pk>/", views.view_pdf, name="view_pdf"),
    path("pdfs/<int:pk>/delete/", views.delete_pdf, name="delete_pdf"),
    path("pdfs/<int:pk>/download/", views.download_pdf, name="download_pdf"),
    # Viewer
    path("viewer/", views.pdf_list, name="pdf_list"),
    path("viewer/about/", views.about, name="about"),
    path("viewer/suggestion/", views.suggestion_view, name="suggestion"),
    path(
        "viewer/suggestion/thanks/",
        views.suggestion_thanks_view,
        name="suggestion_thanks",
    ),
    # Login page
    path("login/", views.index1, name="index1"),
    # Health check
    path("health/", views.health_check, name="health_check"),
]
