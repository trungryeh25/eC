# Generated by Django 3.1 on 2024-10-31 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='product',
        ),
        migrations.DeleteModel(
            name='ReviewRating',
        ),
        migrations.DeleteModel(
            name='Variation',
        ),
    ]
