# Generated by Django 5.2 on 2025-04-11 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0002_ad_is_archived"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ad",
            name="image_url",
        ),
        migrations.AddField(
            model_name="ad",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="uploads/"),
        ),
    ]
