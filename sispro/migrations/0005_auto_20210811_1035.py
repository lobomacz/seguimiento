# Generated by Django 3.2.5 on 2021-08-11 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sispro', '0004_alter_proyecto_programa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protagonistabono',
            name='altura',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='contacto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sispro.contacto'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='programa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sispro.programa'),
        ),
    ]
