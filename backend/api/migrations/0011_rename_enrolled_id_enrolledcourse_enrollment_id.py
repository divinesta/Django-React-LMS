# Generated by Django 5.1.1 on 2024-09-19 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_cartorder_oid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enrolledcourse',
            old_name='enrolled_id',
            new_name='enrollment_id',
        ),
    ]
