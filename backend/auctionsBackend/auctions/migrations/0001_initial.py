# Generated by Django 5.2 on 2025-04-07 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='auction_images/')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('starting_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField()),
                ('rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('brand', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('subasta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pujas', to='auctions.auction')),
            ],
        ),
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
        ),
    ]
