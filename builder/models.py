from random import choices
from django.db import models


class Component(models.Model):
    COMP_TYPES = [
        ('MB', 'Motherboard'),
        ('CPU', 'CPU'),
        ('GPU', 'GPU'),
        ('RAM', 'RAM'),
        ('RF', 'Ref. System'),
        ('CS', 'Case'),
        ('PS', 'Power Supply')
    ]

    c_type = models.CharField(max_length=3 , choices=COMP_TYPES)
    model = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    price = models.FloatField()

    def __str__(self):
        return self.model