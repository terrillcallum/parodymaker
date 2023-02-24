# Generated by Django 3.2.5 on 2021-08-07 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abridging', '0006_alter_snippetsound_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippetsound',
            name='file',
        ),
        migrations.AddField(
            model_name='snippetsound',
            name='file_url',
            field=models.TextField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
