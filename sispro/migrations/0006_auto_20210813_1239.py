# Generated by Django 3.2.5 on 2021-08-13 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sispro', '0005_auto_20210811_1035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='protagonista',
            options={'ordering': ['apellidos', 'nombres'], 'verbose_name': 'Protagonista'},
        ),
        migrations.AddField(
            model_name='capitalizacionplan',
            name='digitador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='protagonista',
            name='digitador',
            field=models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
