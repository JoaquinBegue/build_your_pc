from django.contrib import admin

from .models import *

admin.site.register(Component)
admin.site.register(Motherboard)
admin.site.register(CPU)
admin.site.register(GPU)
admin.site.register(RAM)
admin.site.register(RefSystem)
admin.site.register(Case)
admin.site.register(PowerSupply)
admin.site.register(Order)