# Generated by Django 3.2.5 on 2021-07-28 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abridging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='Character',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='abridging.character'),
        ),
    ]
