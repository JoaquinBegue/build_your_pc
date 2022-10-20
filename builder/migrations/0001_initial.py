# Generated by Django 4.1.2 on 2022-10-20 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_type', models.CharField(choices=[('MB', 'Motherboard'), ('CPU', 'CPU'), ('GPU', 'GPU'), ('RAM', 'RAM'), ('RF', 'Ref. System'), ('CS', 'Case'), ('PS', 'Power Supply')], max_length=3)),
                ('model', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=5000)),
                ('price', models.FloatField()),
            ],
        ),
    ]
