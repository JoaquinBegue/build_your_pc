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

    SOCKETS = [
        ('AMD', 'AMD'),
        ('Intel', 'Intel')
    ]

    c_type = models.CharField(max_length=3 , choices=COMP_TYPES)
    model = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    price = models.FloatField()
    socket = models.CharField(max_length=5, choices=SOCKETS)

    def __str__(self):
        return self.model


class Order(models.Model):
    cpu_brand = models.CharField(max_length=5)
    mb = models.IntegerField(null=True) # motherboard
    cpu = models.IntegerField(null=True)
    gpu = models.IntegerField(null=True)
    ram = models.IntegerField(null=True)
    rf = models.IntegerField(null=True) # ref. system
    cs = models.IntegerField(null=True) # case
    ps = models.IntegerField(null=True) # power supply

    def __str__(self):
        return f"Order No. {self.id}"