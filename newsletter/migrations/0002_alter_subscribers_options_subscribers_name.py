# Generated by Django 4.2.7 on 2023-11-19 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscribers',
            options={'verbose_name_plural': 'Subscribers'},
        ),
        migrations.AddField(
            model_name='subscribers',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
