# Generated by Django 4.2.4 on 2023-11-17 14:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('E_Commerce_app', '0007_alter_comment_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
