# Generated by Django 4.1.7 on 2023-02-28 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("News", "0008_post_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(blank=True),
        ),
    ]