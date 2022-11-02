from django.db import models

class Component(models.Model):
    model = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    price = models.FloatField()
    consumption = models.IntegerField()
    
    def __str__(self):
        return self.model


class Motherboard(Component):
    SOCKETS = [
        ('None', 'None'),
        ('AMD', 'AMD'),
        ('Intel', 'Intel')
    ]

    socket = models.CharField(max_length=5, choices=SOCKETS)
    ram_slots = models.IntegerField(default=0)


class CPU(Component):
    SOCKETS = [
        ('None', 'None'),
        ('AMD', 'AMD'),
        ('Intel', 'Intel')
    ]

    socket = models.CharField(max_length=5, choices=SOCKETS)


class GPU(Component):
    vram = models.IntegerField()

class RAM(Component):
    capacity = models.IntegerField()


class RefSystem(Component):
    number_fans = models.IntegerField()


class Case(Component):
    fan_slots = models.IntegerField()


class PowerSupply(Component):
    potency = models.IntegerField()


class Order(models.Model):
    cpu_brand = models.CharField(max_length=5)
    mb = models.IntegerField(null=True) # motherboard
    cpu = models.IntegerField(null=True)
    gpu = models.IntegerField(null=True)
    ram = models.CharField(max_length=100, null=True)
    rf = models.IntegerField(null=True) # ref. system
    cs = models.IntegerField(null=True) # case
    ps = models.IntegerField(null=True) # power supply

    def __str__(self):
        return f"Order No. {self.id}"