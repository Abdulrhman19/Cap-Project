# Generated by Django 3.1.7 on 2021-04-03 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_auto_20210403_2225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='doctor_id',
            new_name='doctor_email',
        ),
    ]
