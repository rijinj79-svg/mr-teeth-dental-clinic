from django.db import migrations


def add_existing_clinic_doctors(apps, schema_editor):
    Doctor = apps.get_model('clinicapp', 'Doctor')
    known_doctors = [
        {
            'name': 'Dr. Jobu J V',
            'designation': 'Senior Surgeon & Director',
            'image': 'dr.jobu.jpg',
            'display_order': 1,
        },
        {
            'name': 'Dr. Arjun',
            'designation': 'Dental Surgeon',
            'image': 'doctor.png',
            'display_order': 2,
        },
    ]
    for details in known_doctors:
        Doctor.objects.get_or_create(name=details['name'], defaults=details)


def remove_seeded_doctors(apps, schema_editor):
    # Keep these records on rollback so existing clinic data is never deleted.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('clinicapp', '0008_doctor_photo_display_order'),
    ]

    operations = [
        migrations.RunPython(add_existing_clinic_doctors, remove_seeded_doctors),
    ]
