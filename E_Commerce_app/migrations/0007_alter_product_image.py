# Generated by Django 4.2.4 on 2023-09-04 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_Commerce_app', '0006_alter_user_email_alter_user_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='product_images/'),
        ),
    ]
