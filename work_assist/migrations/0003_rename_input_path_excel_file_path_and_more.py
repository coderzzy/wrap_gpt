# Generated by Django 4.2.7 on 2023-12-12 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_assist', '0002_excel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='excel',
            old_name='input_path',
            new_name='file_path',
        ),
        migrations.RemoveField(
            model_name='excel',
            name='output_path',
        ),
    ]
