# Generated by Django 5.0.2 on 2024-02-21 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0002_remove_save_post_remove_save_user_post_saved_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_img',
            field=models.ImageField(default='post_img.jpg', upload_to='post_images'),
        ),
    ]
