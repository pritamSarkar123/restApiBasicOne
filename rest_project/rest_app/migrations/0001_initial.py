# Generated by Django 3.0.8 on 2020-07-23 08:00

from django.db import migrations, models
import rest_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(default=18)),
                ('ranking', models.FloatField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to=rest_app.models.Users.upload_photo)),
                ('resume', models.FileField(blank=True, null=True, upload_to=rest_app.models.Users.upload_file)),
            ],
        ),
    ]