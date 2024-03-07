# Generated by Django 4.2.7 on 2024-03-07 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurent', '0026_food'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='restname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurent', to='Restaurent.restaurent'),
        ),
    ]
