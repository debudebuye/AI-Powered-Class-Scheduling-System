from django.contrib.auth.models import User
from django.test import Client, TestCase

from .forms import InstructorForm, RoomForm, SuggestionForm
from .models import (
    Batch,
    Course,
    Department,
    Instructor,
    MeetingTime,
    Room,
    Section,
    TimeTableModel,
)


class RoomModelTest(TestCase):
    def test_create_room_with_number(self):
        room = Room.objects.create(r_number="R101", seating_capacity=40)
        self.assertEqual(str(room), "R101")
        self.assertEqual(room.seating_capacity, 40)

    def test_auto_generate_room_number(self):
        room = Room.objects.create(seating_capacity=30)
        self.assertEqual(room.r_number, "R001")

    def test_auto_generate_sequential(self):
        Room.objects.create(seating_capacity=30)
        room2 = Room.objects.create(seating_capacity=25)
        self.assertEqual(room2.r_number, "R002")


class InstructorModelTest(TestCase):
    def test_create_instructor(self):
        inst = Instructor.objects.create(uid="I001", name="Dr. Smith")
        self.assertEqual(str(inst), "I001 Dr. Smith")

    def test_auto_generate_uid(self):
        inst = Instructor.objects.create(name="Dr. Jones")
        self.assertEqual(inst.uid, "I001")


class MeetingTimeModelTest(TestCase):
    def test_create_meeting_time(self):
        mt = MeetingTime.objects.create(pid="MT01", time="2:00 - 4:00", day="Monday")
        self.assertEqual(str(mt), "MT01 Monday 2:00 - 4:00")

    def test_auto_generate_pid(self):
        mt = MeetingTime.objects.create(time="4:00 - 6:00", day="Tuesday")
        self.assertEqual(mt.pid, "MT01")

    def test_sort_key(self):
        mt = MeetingTime.objects.create(
            pid="MT01", time="8:00 - 10:00", day="Wednesday"
        )
        key = mt.get_day_sort_key()
        self.assertEqual(key, (2, 2))


class CourseModelTest(TestCase):
    def test_create_course(self):
        course = Course.objects.create(
            course_number="C001", course_name="Math", max_numb_students="60"
        )
        self.assertEqual(str(course), "C001 Math")

    def test_auto_generate_course_number(self):
        course = Course.objects.create(course_name="Science", max_numb_students="45")
        self.assertEqual(course.course_number, "C001")


class DepartmentModelTest(TestCase):
    def test_create_department(self):
        dept = Department.objects.create(dept_name="Computer Science")
        self.assertEqual(str(dept), "Computer Science")


class BatchModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(dept_name="CS")

    def test_create_batch(self):
        batch = Batch.objects.create(
            batch_id="B001",
            batch_name="G2",
            number_of_students=40,
            department=self.dept,
        )
        self.assertEqual(str(batch), "B001 - G2")

    def test_auto_generate_batch_id(self):
        batch = Batch.objects.create(
            batch_name="G3", number_of_students=35, department=self.dept
        )
        self.assertEqual(batch.batch_id, "B001")


class SectionModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(dept_name="CS")
        self.batch = Batch.objects.create(
            batch_name="G2", number_of_students=40, department=self.dept
        )

    def test_create_section(self):
        sec = Section.objects.create(
            section_id="S001", batch=self.batch, num_class_in_week=3
        )
        self.assertEqual(sec.section_id, "S001")

    def test_auto_generate_section_id(self):
        sec = Section.objects.create(batch=self.batch, num_class_in_week=2)
        self.assertEqual(sec.section_id, "S001")


class TimeTableModelTest(TestCase):
    def test_create_timetable_entry(self):
        entry = TimeTableModel.objects.create(
            section="S001",
            batch="G2",
            course="Math",
            venue="R101",
            instructor="Dr. Smith",
            clstime="Monday 2:00 - 4:00",
        )
        self.assertEqual(entry.section, "S001")


class RoomFormTest(TestCase):
    def test_valid_form(self):
        form = RoomForm(data={"r_number": "R101", "seating_capacity": 40})
        self.assertTrue(form.is_valid())

    def test_auto_generate_form(self):
        form = RoomForm(data={"r_number": "", "seating_capacity": 40})
        self.assertTrue(form.is_valid())


class InstructorFormTest(TestCase):
    def test_valid_form(self):
        form = InstructorForm(data={"uid": "", "name": "Dr. Smith"})
        self.assertTrue(form.is_valid())

    def test_duplicate_name(self):
        Instructor.objects.create(name="Dr. Smith")
        form = InstructorForm(data={"name": "Dr. Smith"})
        self.assertFalse(form.is_valid())


class ScheduleViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="admin", password="adminpass123", is_staff=True
        )

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_admindash_requires_login(self):
        response = self.client.get("/admin-dashboard/")
        self.assertEqual(response.status_code, 302)

    def test_admindash_with_login(self):
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get("/admin-dashboard/")
        self.assertEqual(response.status_code, 200)

    def test_add_instructor_page(self):
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get("/teachers/add/")
        self.assertEqual(response.status_code, 200)

    def test_add_room_page(self):
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get("/rooms/add/")
        self.assertEqual(response.status_code, 200)

    def test_suggestion_page(self):
        response = self.client.get("/viewer/suggestion/")
        self.assertEqual(response.status_code, 200)


class SuggestionFormTest(TestCase):
    def test_valid_form(self):
        form = SuggestionForm(
            data={
                "name": "Test User",
                "email": "test@example.com",
                "suggestion": "Great system!",
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = SuggestionForm(
            data={
                "name": "Test",
                "email": "not-an-email",
                "suggestion": "Hello",
            }
        )
        self.assertFalse(form.is_valid())
