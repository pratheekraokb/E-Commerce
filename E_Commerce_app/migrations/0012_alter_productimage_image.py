# Generated by Django 4.2.4 on 2023-09-06 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_Commerce_app', '0011_alter_productimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='shop/additional_images/'),
        ),
    ]
