# Generated by Django 4.1.5 on 2023-02-17 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0002_alter_user_email_alter_user_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user", name="password", field=models.CharField(max_length=1000),
        ),
    ]
