# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_tokenpassword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenpassword',
            name='used_at',
            field=models.DateTimeField(verbose_name='date creation', blank=True, null=True),
        ),
    ]
