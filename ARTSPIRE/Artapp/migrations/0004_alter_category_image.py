# Generated by Django 5.0.1 on 2024-02-28 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Artapp', '0003_alter_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
