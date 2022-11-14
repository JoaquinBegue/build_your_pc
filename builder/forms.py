from django import forms


class ComponentForm(forms.Form):
    def __init__(self, choices, label, required, *args, **kwargs):
        self.base_fields['comp'].choices = choices
        self.base_fields['comp'].label = label
        self.base_fields['comp'].required = required
        super(ComponentForm, self).__init__(*args, **kwargs)

    comp = forms.ChoiceField(widget=forms.RadioSelect, choices=())
    
    
class RamForm(forms.Form):
    def __init__(self, choices, label, max_amount, *args, **kwargs):
        self.base_fields['comp'].choices = choices
        self.base_fields['comp'].label = label
        self.base_fields['amount'] = forms.IntegerField(min_value=1,
            max_value=max_amount, required=False)
        super(RamForm, self).__init__(*args, **kwargs)

    comp = forms.ChoiceField(widget=forms.RadioSelect, choices=(),
        required=False)
    amount = forms.IntegerField()