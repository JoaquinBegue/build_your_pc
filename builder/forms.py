from django import forms


class ComponentForm(forms.Form):
    def __init__(self, choices, label, *args, **kwargs):
        self.base_fields['comp'].choices = choices
        self.base_fields['comp'].label = label
        super(ComponentForm, self).__init__(*args, **kwargs)

    comp = forms.ChoiceField(widget=forms.RadioSelect, choices=(), required=True)
    
    
    

    