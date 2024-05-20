# Generated by Django 4.2.11 on 2024-05-20 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MojaStrona', '0003_alter_extrainfo_gatunek'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrainfo',
            name='gatunek',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(4, 'Dramat'), (1, 'Horror'), (0, 'Inne'), (3, 'Sci-fi'), (2, 'Komedia')], null=True),
        ),
    ]