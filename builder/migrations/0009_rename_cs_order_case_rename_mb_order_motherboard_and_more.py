# Generated by Django 4.1.2 on 2022-11-10 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0008_alter_cpu_socket'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='cs',
            new_name='case',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='mb',
            new_name='motherboard',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='ps',
            new_name='power_supply',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='rf',
            new_name='ref_system',
        ),
    ]
