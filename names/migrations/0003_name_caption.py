# Generated by Django 3.1 on 2022-02-03 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('names', '0002_name_excluded'),
    ]

    operations = [
        migrations.AddField(
            model_name='name',
            name='caption',
            field=models.TextField(blank=True, default=''),
        ),
    ]
