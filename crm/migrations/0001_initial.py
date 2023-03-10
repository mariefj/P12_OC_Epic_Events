# Generated by Django 4.1.5 on 2023-01-18 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
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
                ("first_name", models.CharField(max_length=150)),
                ("last_name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=20, unique=True)),
                ("mobile", models.CharField(max_length=20, unique=True)),
                ("company_name", models.CharField(max_length=250)),
                ("date_created", models.DateField(auto_now_add=True)),
                ("date_updated", models.DateField(auto_now=True)),
                (
                    "sales_contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="client",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Event",
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
                ("date_created", models.DateField(auto_now_add=True)),
                ("date_updated", models.DateField(auto_now=True)),
                ("attendees", models.IntegerField()),
                ("notes", models.TextField()),
                ("event_date", models.DateTimeField()),
                (
                    "event_status",
                    models.CharField(
                        choices=[("In progress", "In progress"), ("Done", "Done")],
                        default="In progress",
                        max_length=25,
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event",
                        to="crm.client",
                    ),
                ),
                (
                    "support_contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Contract",
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
                ("date_created", models.DateField(auto_now_add=True)),
                ("date_updated", models.DateField(auto_now=True)),
                ("amount", models.FloatField()),
                ("status", models.BooleanField(default=False, verbose_name="signed")),
                ("payment_due", models.DateField(null=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contract",
                        to="crm.client",
                    ),
                ),
                (
                    "sales_contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contract",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
