# Generated by Django 5.0.6 on 2024-07-20 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_cartitem_unique_together_alter_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.customer'),
        ),
    ]
