# Generated by Django 3.1.7 on 2021-03-14 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210314_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patinet',
            name='supervised_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.doctor'),
        ),
    ]