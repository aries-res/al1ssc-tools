# Generated by Django 3.2.6 on 2021-08-30 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orbit_tool', '0002_auto_20210830_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='body',
            name='color',
            field=models.CharField(max_length=200),
        ),
    ]
