# Generated by Django 2.2.5 on 2020-01-22 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0004_auto_20200122_1938'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emails',
            old_name='Email',
            new_name='email_adress',
        ),
    ]
