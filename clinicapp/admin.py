from django.contrib import admin
from .models import Appointment, Contact, Doctor, Patient, GalleryMedia, Feedback,Department


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "qualification", "active", "display_order")
    list_filter = ("active",)
    ordering = ("display_order", "name")
    search_fields = ("name", "designation", "qualification")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "service", "doctor", "appointment_date", "appointment_time", "status", "created_at")
    list_filter = ("status", "service", "doctor", "appointment_date", "gender")
    search_fields = ("name", "phone", "email", "place", "patient__username")
    ordering = ("appointment_date", "appointment_time")
    list_editable = ("status",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "phone", "message")
    list_editable = ("status",)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("op_no", "name", "phone", "date")
    search_fields = ("op_no", "name", "phone")


@admin.register(GalleryMedia)
class GalleryMediaAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "description")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "rating", "created_at")
    search_fields = ("name", "message")
    list_editable = ("is_approved",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "short_description",
        "is_active",
        "display_order",
    )

    list_filter = ("is_active",)
    search_fields = ("name", "short_description")
    list_editable = ("is_active", "display_order")
