# Generated by Django 5.0.1 on 2024-02-23 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('Description', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('creationDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ScamReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporterID', models.CharField(max_length=50)),
                ('reportedUserID', models.CharField(max_length=50)),
                ('report', models.TextField()),
                ('timeStamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalSales', models.DecimalField(decimal_places=2, max_digits=10)),
                ('successAuctions', models.IntegerField()),
                ('portfolio', models.BinaryField()),
                ('verified', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('userType', models.CharField(max_length=10)),
                ('mobileNo', models.CharField(max_length=15)),
                ('bDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalBids', models.IntegerField()),
                ('favourites', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Artapp.artwork')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Artapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bidTimeStamp', models.DateTimeField()),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Artapp.artwork')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids_buyer', to='Artapp.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('basePrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('auctionStatus', models.BooleanField()),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Artapp.artwork')),
                ('participants', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Artapp.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchaseAmt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchaseTime', models.DateTimeField()),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Artapp.artwork')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_history_buyer', to='Artapp.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timeStamp', models.DateTimeField()),
                ('status', models.BooleanField()),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Artapp.seller')),
            ],
        ),
        migrations.AddField(
            model_name='artwork',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artworks_seller', to='Artapp.seller'),
        ),
        migrations.AddField(
            model_name='seller',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Artapp.user'),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissions', models.CharField(max_length=255)),
                ('activityTimeStamp', models.DateTimeField()),
                ('user', models.ManyToManyField(to='Artapp.user')),
            ],
        ),
    ]