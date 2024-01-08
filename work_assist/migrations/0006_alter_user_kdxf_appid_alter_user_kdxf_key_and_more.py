# Generated by Django 4.2.7 on 2024-01-08 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_assist', '0005_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='kdxf_appid',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='kdxf_key',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='kdxf_secret',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='openai_3_5_key',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='openai_4_key',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='wenxin_token',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]