# Generated by Django 4.1.3 on 2022-12-02 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='track',
            old_name='track',
            new_name='file',
        ),
    ]
