# Generated by Django 5.2.1 on 2025-05-10 18:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="fecha_creacion",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="fecha_modificacion",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
