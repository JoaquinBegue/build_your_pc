from random import choices
from django import forms

from .models import *

class BrandForm(forms.Form):
    CHOICES = [('amd', 'AMD'), ('intel', 'Intel')]
    brand = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, 
        label="To start, select a brand for your CPU:")


class CpuForm(forms.Form):
    def __init__(self, cpu_choices, *args, **kwargs):
        super(CpuForm, self).__init__(*args, **kwargs)
        self.fields['cpu'].choices = cpu_choices

    cpu = forms.ChoiceField(widget=forms.RadioSelect, choices=(), required=True)
    
    
    

    