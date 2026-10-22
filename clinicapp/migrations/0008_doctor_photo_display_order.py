from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('clinicapp', '0007_gallerymedia_feedback_walkin_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='doctors/'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='display_order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'ordering': ['display_order', 'name']},
        ),
    ]
