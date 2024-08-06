from django import forms
from django.forms import inlineformset_factory
from .models import CreditCard, BillingAddress
from datetime import datetime

class MonthYearWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        current_year = datetime.now().year
        year_choices = [(i, i) for i in range(current_year, current_year + 11)]
        widgets = [
            forms.Select(attrs=attrs, choices=[(i, i) for i in range(1, 13)]), 
            forms.Select(attrs=attrs, choices=year_choices),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.month, value.year]
        return [None, None]

class MonthYearField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        current_year = datetime.now().year
        year_choices = [(i, i) for i in range(current_year, current_year + 11)] 
        fields = [
            forms.ChoiceField(choices=[(i, i) for i in range(1, 13)]),
            forms.ChoiceField(choices=year_choices), 
        ]
        super().__init__(fields, widget=MonthYearWidget(), *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            month, year = data_list
            if month and year:
                return datetime(int(year), int(month), 1).date()
        return None

class CreditCardForm(forms.ModelForm):
    expiration_date = MonthYearField()

    class Meta:
        model = CreditCard
        fields = ['card_holder', 'card_number', 'expiration_date', 'cvv']

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country']

# Inline formset to combine CreditCardForm and BillingAddressForm
CreditCardFormSet = inlineformset_factory(CreditCard, BillingAddress, form=BillingAddressForm, extra=1, can_delete=False)
