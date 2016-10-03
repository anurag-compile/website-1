# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-17 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_auto_20160328_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfield',
            name='choices',
            field=models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices'),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='to_address',
            field=models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, verbose_name='to address'),
        ),
    ]