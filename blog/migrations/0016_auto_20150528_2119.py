# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20150526_2252'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AboutPage',
        ),
        migrations.DeleteModel(
            name='ContactPage',
        ),
    ]
