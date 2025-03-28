from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField


ROLE_CHOICES = (
    ('doctor', 'doctor'),
    ('patient', 'patient')
)


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),
                                                       MaxValueValidator(75)], null=True, blank=True)
    profile = models.ImageField(upload_to='profiles/', null=True, blank=True)
    gender = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Department(models.Model):
    department_name = models.CharField(max_length=32)
    level = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])

    def __str__(self):
        return self.department_name


class Specialty(models.Model):
    specialty_name = models.CharField(max_length=64)

    def __str__(self):
        return self.specialty_name


class Doctor(UserProfile):
    DAY_CHOICES = (
        ('ПН', 'ПН'),
        ('ВТ', 'ВТ'),
        ('СР', 'СР'),
        ('ЧТ', 'ЧТ'),
        ('ПТ', 'ПТ'),
        ('СБ', 'СБ'),
    )
    work_day = MultiSelectField(choices=DAY_CHOICES, max_choices=6, max_length=32)
    experience = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(80)])
    specialty = models.ManyToManyField(Specialty, null=True, blank=True, related_name='doctor_specialty')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctor_department')
    bio = models.TextField(null=True, blank=True)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    service_price = models.PositiveSmallIntegerField(validators=[MinValueValidator(500),
                                                                 MaxValueValidator(1500)], null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=16, default='doctor')

    def __str__(self):
        return f'{self.first_name}, {self.specialty}'

    def get_count_comment(self):
        total = self.doctor_feed.all()
        if total.exists():
            return total.count()
        return 0

    def get_avg_rating(self):
        total = self.doctor_feed.all()
        if total.exists():
            return round(sum([i.rating for i in total]) / total.count(), 1)


    class Meta:
        verbose_name= 'doctor'
        verbose_name_plural = "doctor"


class Patient(UserProfile):
    emergency_contact = PhoneNumberField()
    BLOOD_CHOICES = (
        ('I+', 'I+'),
        ('I-', 'I-'),
        ('II+', 'II+'),
        ('II-', 'II-'),
        ('III+', 'III+'),
        ('III-', 'III-'),
        ('IV+', 'IV+'),
        ('IV-', 'IV-'),
    )
    blood_type = models.CharField(choices=BLOOD_CHOICES, max_length=8)
    role = models.CharField(choices=ROLE_CHOICES, max_length=16, default='patient')

    def __str__(self):
        return f'{self.first_name}, {self.role}'

    class Meta:
        verbose_name= 'patient'
        verbose_name_plural = "patient"



class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointment_patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointment_doctor')
    date_time = models.DateTimeField()
    STATUS_CHOICES = (
        ('запланировано', 'запланировано',),
        ('завершено', 'завершено',),
        ('отменено', 'отменено',),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=32)

    def __str__(self):
        return f'{self.patient}, {self.status}'


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescribed_medication = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient}, {self.doctor}'


class Feedback(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_feed')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True )
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.doctor}, {self.rating}'


class Ward(models.Model):
    room_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)], null=True, blank=True)
    TYPE_CHOICES = (
        ('Vip', 'Vip'),
        ('Simple', 'Simple'),
        ('Medium', 'Medium')
    )
    type_ward = models.CharField(max_length=16, choices=TYPE_CHOICES)
    total_people = models.PositiveSmallIntegerField(validators=[MaxValueValidator(8)])
    current_people = models.PositiveSmallIntegerField(validators=[MaxValueValidator(8)])

    def __str__(self):
        return f'{self.room_number}, {self.type_ward}'

    def get_count_people(self):
        total = self.total_people
        current = self.current_people
        if total == current:
            return f'место жок калды'

        else:
            return f'{total - current} место бар'


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='chat_images', null=True, blank=True)
    video = models.FileField(upload_to='chat_videos', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
