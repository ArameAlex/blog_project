# Generated by Django 4.2.4 on 2024-03-29 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_post_tag_tag_alter_post_tag_tag_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post_tag',
            name='tag_url',
            field=models.SlugField(blank=True, max_length=150, unique=True),
        ),
    ]
