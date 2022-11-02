# Generated by Django 4.1.1 on 2022-10-31 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0002_alter_order_ram'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refsystem',
            name='coverage',
        ),
        migrations.AddField(
            model_name='refsystem',
            name='number_fans',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
