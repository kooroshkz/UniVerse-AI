# Generated by Django 5.1.2 on 2024-12-12 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatbot", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("course_name", models.CharField(max_length=255)),
                ("course_type", models.CharField(max_length=50)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("locations", models.TextField()),
                ("staffs", models.TextField()),
            ],
        ),
    ]
