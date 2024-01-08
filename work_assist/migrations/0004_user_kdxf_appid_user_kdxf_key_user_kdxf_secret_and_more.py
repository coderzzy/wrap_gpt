# Generated by Django 4.2.7 on 2024-01-08 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_assist', '0003_rename_input_path_excel_file_path_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='kdxf_appid',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='kdxf_key',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='kdxf_secret',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='openai_3_5_key',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='openai_4_key',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='wenxin_token',
            field=models.CharField(default='', max_length=255),
        ),
    ]