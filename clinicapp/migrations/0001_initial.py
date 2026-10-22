from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Doctor", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=120)), ("designation", models.CharField(max_length=150)),
            ("qualification", models.CharField(blank=True, max_length=200)), ("bio", models.TextField(blank=True)),
            ("image", models.CharField(blank=True, default="doctor.png", max_length=255)), ("active", models.BooleanField(default=True)),
        ], options={"ordering": ["name"]}),
        migrations.CreateModel(name="Contact", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=100)), ("age", models.PositiveIntegerField(blank=True, null=True)),
            ("gender", models.CharField(blank=True, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")], max_length=10)),
            ("place", models.CharField(blank=True, max_length=100)), ("phone", models.CharField(max_length=15)),
            ("email", models.EmailField(max_length=254)), ("message", models.TextField()),
            ("status", models.CharField(choices=[("New", "New"), ("Read", "Read"), ("Replied", "Replied")], default="New", max_length=20)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
        ], options={"ordering": ["-created_at"]}),
        migrations.CreateModel(name="Appointment", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=100)), ("age", models.PositiveIntegerField()),
            ("gender", models.CharField(choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")], max_length=10)),
            ("place", models.CharField(max_length=100)), ("phone", models.CharField(max_length=15)),
            ("email", models.EmailField(blank=True, max_length=254)),
            ("service", models.CharField(choices=[("Dental Consultation", "Dental Consultation"), ("Teeth Cleaning", "Teeth Cleaning"), ("Teeth Whitening", "Teeth Whitening"), ("Root Canal Treatment", "Root Canal Treatment"), ("General Dentistry", "General Dentistry")], default="Dental Consultation", max_length=50)),
            ("appointment_date", models.DateField()), ("appointment_time", models.TimeField()), ("message", models.TextField(blank=True)),
            ("status", models.CharField(choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Completed", "Completed"), ("Cancelled", "Cancelled")], default="Pending", max_length=20)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("doctor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="appointments", to="clinicapp.doctor")),
            ("patient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="appointments", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ["-appointment_date", "-appointment_time"]}),
        migrations.AddIndex(model_name="appointment", index=models.Index(fields=["appointment_date", "appointment_time"], name="clinicapp_ap_appointm_8f1c25_idx")),
        migrations.AddIndex(model_name="appointment", index=models.Index(fields=["status"], name="clinicapp_ap_status_4e3a3c_idx")),
    ]
