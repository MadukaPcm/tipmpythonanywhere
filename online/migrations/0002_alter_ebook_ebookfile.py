# Generated by Django 3.2.15 on 2022-11-10 12:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebook',
            name='eBookFile',
            field=models.FileField(blank=True, null=True, upload_to='onlineeBook', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]