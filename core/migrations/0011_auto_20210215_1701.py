# Generated by Django 3.1.6 on 2021-02-15 16:01

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210214_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
