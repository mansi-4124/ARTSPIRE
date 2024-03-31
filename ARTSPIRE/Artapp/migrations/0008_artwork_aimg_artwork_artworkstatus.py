# Generated by Django 5.0.1 on 2024-02-29 09:52

import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Artapp', '0007_alter_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='aimg',
            field=django_resized.forms.ResizedImageField(crop=None, default='/static/img/default-artwork.jpg', force_format='JPEG', keep_meta=True, quality=75, scale=None, size=[262, 280], upload_to=''),
        ),
        migrations.AddField(
            model_name='artwork',
            name='artworkStatus',
            field=models.BooleanField(default=True),
        ),
    ]
