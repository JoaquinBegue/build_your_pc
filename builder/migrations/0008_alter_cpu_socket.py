# Generated by Django 4.1.2 on 2022-11-02 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0007_alter_cpu_socket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='socket',
            field=models.CharField(choices=[('None', 'None'), ('AMD', 'AMD'), ('Intel', 'Intel')], max_length=5),
        ),
    ]
