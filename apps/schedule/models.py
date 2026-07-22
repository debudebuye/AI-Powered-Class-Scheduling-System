from django.db import models

time_slots = (
    ("2:00 - 4:00", "2:00 - 4:00"),
    ("4:00 - 6:00", "4:00 - 6:00"),
    ("8:00 - 10:00", "8:00 - 10:00"),
)

DAYS_OF_WEEK = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
)

BATCH = (
    ("G2", "G2"),
    ("G3", "G3"),
    ("G4", "G4"),
    ("G5", "G5"),
)

DEPARTMENT = (
    ("CS", "CS"),
    ("IT", "IT"),
    ("SE", "SE"),
)

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class Room(models.Model):
    r_number = models.CharField(max_length=6, unique=True, blank=True)
    seating_capacity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.r_number:
            # Auto-generate room number if not provided
            last_room = (
                Room.objects.filter(r_number__startswith="R")
                .order_by("r_number")
                .last()
            )
            if last_room:
                try:
                    last_num = int(last_room.r_number[1:])
                    self.r_number = f"R{last_num + 1:03d}"
                except ValueError:
                    self.r_number = "R001"
            else:
                self.r_number = "R001"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.r_number


class Instructor(models.Model):
    uid = models.CharField(max_length=6, unique=True, blank=True)
    name = models.CharField(max_length=25)

    def save(self, *args, **kwargs):
        if not self.uid:
            # Auto-generate instructor ID if not provided
            last_instructor = (
                Instructor.objects.filter(uid__startswith="I").order_by("uid").last()
            )
            if last_instructor:
                try:
                    last_num = int(last_instructor.uid[1:])
                    self.uid = f"I{last_num + 1:03d}"
                except ValueError:
                    self.uid = "I001"
            else:
                self.uid = "I001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.uid} {self.name}"


class MeetingTime(models.Model):
    pid = models.CharField(max_length=4, primary_key=True)
    time = models.CharField(max_length=50, choices=time_slots, default="2:00 - 4:00")
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)

    def save(self, *args, **kwargs):
        if not self.pid:
            # Auto-generate meeting time ID if not provided
            last_mt = (
                MeetingTime.objects.filter(pid__startswith="MT").order_by("pid").last()
            )
            if last_mt:
                try:
                    last_num = int(last_mt.pid[2:])
                    self.pid = f"MT{last_num + 1:02d}"
                except ValueError:
                    self.pid = "MT01"
            else:
                self.pid = "MT01"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pid} {self.day} {self.time}"

    def get_day_sort_key(self):
        days_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        times_order = [
            "2:00 - 4:00",
            "4:00 - 6:00",
            "8:00 - 10:00",
        ]  # Define the order of time slots

        # Get index for day and time
        day_index = days_order.index(self.day)
        time_index = times_order.index(self.time)

        # Return a tuple that combines day and time index
        return (day_index, time_index)


class Course(models.Model):
    course_number = models.CharField(max_length=5, primary_key=True)
    course_name = models.CharField(max_length=40)
    max_numb_students = models.PositiveIntegerField(default=60)
    instructors = models.ManyToManyField(Instructor, blank=True)

    def save(self, *args, **kwargs):
        if not self.course_number:
            # Auto-generate course number if not provided
            last_course = (
                Course.objects.filter(course_number__startswith="C")
                .order_by("course_number")
                .last()
            )
            if last_course:
                try:
                    last_num = int(last_course.course_number[1:])
                    self.course_number = f"C{last_num + 1:03d}"
                except ValueError:
                    self.course_number = "C001"
            else:
                self.course_number = "C001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_number} {self.course_name}"


class Department(models.Model):
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return self.dept_name


class Batch(models.Model):
    batch_id = models.CharField(max_length=10, unique=True, blank=True)
    batch_name = models.CharField(max_length=255, default="")
    number_of_students = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    courses = models.ManyToManyField(
        Course, blank=True
    )  # Associate courses with batches

    def save(self, *args, **kwargs):
        if not self.batch_id:
            # Auto-generate batch ID if not provided
            last_batch = (
                Batch.objects.filter(batch_id__startswith="B")
                .order_by("batch_id")
                .last()
            )
            if last_batch:
                try:
                    last_num = int(last_batch.batch_id[1:])
                    self.batch_id = f"B{last_num + 1:03d}"
                except ValueError:
                    self.batch_id = "B001"
            else:
                self.batch_id = "B001"
        super().save(*args, **kwargs)

    @property
    def get_courses(self):
        return self.courses

    def __str__(self):
        return f"{self.batch_id} - {self.batch_name}"


class Section(models.Model):
    section_id = models.CharField(max_length=25, primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    num_class_in_week = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    meeting_time = models.ForeignKey(
        MeetingTime, on_delete=models.CASCADE, blank=True, null=True
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if not self.section_id:
            # Auto-generate section ID if not provided
            last_section = (
                Section.objects.filter(section_id__startswith="S")
                .order_by("section_id")
                .last()
            )
            if last_section:
                try:
                    last_num = int(last_section.section_id[1:])
                    self.section_id = f"S{last_num + 1:03d}"
                except ValueError:
                    self.section_id = "S001"
            else:
                self.section_id = "S001"
        super().save(*args, **kwargs)

    def set_room(self, room):
        section = Section.objects.get(pk=self.section_id)
        section.room = room
        section.save()

    def set_meetingTime(self, meetingTime):
        section = Section.objects.get(pk=self.section_id)
        section.meeting_time = meetingTime
        section.save()

    def set_instructor(self, instructor):
        section = Section.objects.get(pk=self.section_id)
        section.instructor = instructor
        section.save()


class TimeTableModel(models.Model):
    section = models.CharField(max_length=100)
    batch = models.CharField(max_length=100)  # Update to use batch
    course = models.CharField(max_length=50)
    venue = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    clstime = models.CharField(max_length=100)


class PDF(models.Model):
    title = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to="pdfs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.file.name
