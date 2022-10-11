# Generated by Django 4.1.2 on 2022-10-10 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("account", "0007_customer_profile_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="profile_pic",
            field=models.ImageField(
                blank=True, default="avatar.png", null=True, upload_to=""
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
