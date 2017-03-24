from django import forms
from django.forms import ModelForm
from .models import Customer

class DateInput(forms.DateInput):
    input_type = 'date'
    
class CustomerCreationForm(forms.ModelForm):
    #DATE_OF_BIRTH = forms.DateField(widget=DateInput())
    #DATE_REG = forms.DateField(widget=DateInput())
    class Meta:
        model = Customer
        fields = [
            "CUSTOMER_NAME",
            "DATE_OF_BIRTH",
            "AGE_GROUP",
            "GENDER",
            "PREF_LANG_1",
            "PREF_LANG_2",
            "USER_TYPE",
            "DATE_REG",
        ]
        widgets = {
            'DATE_OF_BIRTH': DateInput(),
        }
