# Generated by Django 4.2.7 on 2024-03-05 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurent', '0009_transactions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookings',
            options={'ordering': ['-id']},
        ),
    ]
