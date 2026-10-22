from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Doctor(models.Model):
    name = models.CharField(max_length=120)
    designation = models.CharField(max_length=150)
    qualification = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    image = models.CharField(max_length=255, blank=True, default="doctor.png")
    photo = models.ImageField(upload_to="doctors/", blank=True, null=True)
    active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name

class Patient(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    op_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date = models.DateField()
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    class Meta:
        ordering = ["date", "op_no"]

    def __str__(self):
        return f"{self.op_no} - {self.name}"

class Appointment(models.Model):

    # Link appointment to a registered Patient record
    patient_record = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointment_records"
    )

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    SERVICE_CHOICES = [
        ("Dental Consultation", "Dental Consultation"),
        ("Teeth Cleaning", "Teeth Cleaning"),
        ("Teeth Whitening", "Teeth Whitening"),
        ("Root Canal Treatment", "Root Canal Treatment"),
        ("General Dentistry", "General Dentistry"),
    ]

    # Django login user who booked the appointment
    patient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="appointments",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=100)

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    place = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    service = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES,
        default="Dental Consultation"
    )

    doctor = models.ForeignKey(
        "clinicapp.Doctor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments"
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-appointment_date",
            "-appointment_time"
        ]

        indexes = [
            models.Index(
                fields=[
                    "appointment_date",
                    "appointment_time"
                ]
            ),
            models.Index(
                fields=["status"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.name} - "
            f"{self.appointment_date} "
            f"{self.appointment_time}"
        )

class Contact(models.Model):
    STATUS_CHOICES = [("New", "New"), ("Read", "Read"), ("Replied", "Replied")]
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Appointment.GENDER_CHOICES, blank=True)
    place = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="New")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"

class FinanceIncome(models.Model):

    payment_date = models.DateField(
        default=timezone.localdate
    )

    op_no = models.CharField(
        max_length=20,
        blank=True
    )

    patient_name = models.CharField(
    max_length=100,
    default=""
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=10,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other"),
        ],
        blank=True
    )

    doctor_name = models.CharField(
        max_length=120,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    procedure = models.CharField(
        max_length=150
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=[
            ("Cash", "Cash"),
            ("UPI", "UPI"),
            ("Card", "Card"),
            ("Other", "Other"),
        ],
        default="Cash"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-payment_date",
            "-id"
        ]

    def __str__(self):

        return (
            f"{self.op_no} - "
            f"{self.patient_name} - "
            f"â‚¹{self.amount}"
        )

class FinanceExpense(models.Model):

    expense_date = models.DateField(
        default=timezone.localdate
    )

    description = models.CharField(
        max_length=200
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "-expense_date",
            "-id"
        ]

    def __str__(self):
        return f"{self.description} - â‚¹{self.amount}"


class GalleryMedia(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="gallery/images/", blank=True, null=True)
    video = models.FileField(upload_to="gallery/videos/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Gallery media"
        verbose_name_plural = "Gallery media"

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        if bool(self.image) == bool(self.video):
            raise ValidationError("Upload either one image or one video, not both.")


class Feedback(models.Model):
    RATING_CHOICES = [(i, f"{i} star{'s' if i != 1 else ''}") for i in range(1, 6)]
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    message = models.TextField(max_length=1200)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.rating}/5"
class StaffProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )
    photo = models.ImageField(
        upload_to="staff/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Profile - {self.user.username}"


from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)

    short_description = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    specialities = models.TextField(
        blank=True,
        help_text="Enter the specialities offered by this department."
    )

    treatments = models.TextField(
        blank=True,
        help_text="Enter the available treatments."
    )

    # Choose an image file from your computer
    image = models.ImageField(
        upload_to="departments/",
        blank=True,
        null=True
    )

    # Kept for compatibility with existing website code
    image_url = models.URLField(blank=True)

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    icon = models.CharField(
        max_length=60,
        default="bi-tooth",
        help_text="Bootstrap Icon class, e.g. bi-tooth"
    )

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name
