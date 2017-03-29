from django import forms
from django.forms import ModelForm
from pingow_api.models import *

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

class CustomerForm(forms.ModelForm):
    CUSTOMER_ID = forms.IntegerField(disabled=True)
    class Meta:
        model = Customer
        fields = [
            "CUSTOMER_ID",
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


class AssistanceForm(forms.ModelForm):
    PHOTO_URL = forms.CharField(required=False)
    ASST_ID = forms.IntegerField(disabled=True)
    class Meta:
        model = Assistance
        fields = [
            'ASST_ID',
            'SHOP_ID',
            'ASST_NAME',
            'DATE_OF_BIRTH',
            'AGE_GROUP',
            'GENDER',
            'PREF_LANG_1',
            'PREF_LANG_2',
            'TRAINED_SKILL',
            'TRAINED_LEVEL',
            'PRODUCT_SKILL',
            'PHOTO_URL',
        ]

class CustomerTransactionForm(forms.ModelForm):
    TRANSACTION_ID = forms.IntegerField(disabled=True)
    TIME_OF_EXIT = forms.DateTimeField(required=False)
    class Meta:
        model = CustomerTransaction
        fields = [
            'TRANSACTION_ID',
            'CUSTOMER_ID',
            'SUB_CAT_ID',
            'SHOP_ID',
            'ASST_ID',
            'CREATION_DATE',
            'TIME_OF_ENTER',
            'TIME_OF_EXIT',
            'ASST_SVC_RATE',
            'OVERALL_RATE',
            'COMMENTS',
        ]
