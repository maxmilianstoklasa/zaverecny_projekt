from django import forms


class AvailabilityForm(forms.Form):
    check_in = forms.DateField(required=True, input_formats=['%Y-%m-%d', ])
    check_out = forms.DateField(required=True, input_formats=['%Y-%m-%d', ])

    def print_form(self):
        pass
