# Generated by Django 3.2.15 on 2022-11-12 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_auto_20221019_0819'),
        ('online', '0002_alter_ebook_ebookfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebook',
            name='categoryId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='category_e_Book', to='book.category'),
        ),
        migrations.AddField(
            model_name='ebook',
            name='publisher',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ebook',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ebook',
            name='yearOfPublication',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]