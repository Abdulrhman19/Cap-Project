# Generated by Django 3.1.7 on 2021-04-11 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='personal_image',
            field=models.ImageField(default='default.jpg', upload_to='user_pics'),
        ),
    ]