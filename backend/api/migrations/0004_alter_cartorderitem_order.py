# Generated by Django 5.1.1 on 2024-09-12 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_course_teacher_course_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitem', to='api.cartorder'),
        ),
    ]
