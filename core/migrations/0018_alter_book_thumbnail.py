# Generated by Django 5.0.6 on 2024-07-14 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_book_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='thumbnail',
            field=models.ImageField(default='static/images/KK_logo.jpeg', upload_to='static/images/'),
        ),
    ]
