# Generated by Django 4.2.7 on 2024-03-01 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurent', '0006_rename_person_bookings_persons'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='tabelno',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='persons',
            name='tabelno',
            field=models.IntegerField(default=0),
        ),
    ]
