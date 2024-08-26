# Generated by Django 5.1 on 2024-08-24 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_otp_email_remove_otp_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='email',
            field=models.EmailField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='otp',
            name='password',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
