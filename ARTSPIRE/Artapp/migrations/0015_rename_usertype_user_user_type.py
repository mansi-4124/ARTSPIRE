# Generated by Django 5.0.1 on 2024-03-15 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Artapp', '0014_remove_user_bdate_remove_user_mobileno_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='userType',
            new_name='user_type',
        ),
    ]