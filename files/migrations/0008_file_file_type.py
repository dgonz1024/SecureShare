# Generated by Django 3.2.25 on 2025-04-10 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_auto_20250410_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
