# Generated by Django 5.0.1 on 2024-03-30 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Artapp', '0020_auction_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyauction',
            name='auction',
        ),
        migrations.RemoveField(
            model_name='buyauction',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='seller',
        ),
        migrations.DeleteModel(
            name='ScamReport',
        ),
        migrations.DeleteModel(
            name='BuyAuction',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
