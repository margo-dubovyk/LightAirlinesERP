# Generated by Django 4.1.1 on 2022-09-22 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0001_initial'),
        ('account', '0002_staffprofile_passengerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='airport',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='airline.airport'),
        ),
    ]