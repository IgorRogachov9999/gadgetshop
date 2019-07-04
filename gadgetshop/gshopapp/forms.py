from django import forms
from django.utils import timezone
from gshopapp.models import DELIVERY_CHOICES


class OrderForm(forms.Form):

    name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=DELIVERY_CHOICES)
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea(), required=False)


    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Name'
        self.fields['last_name'].label = 'Last name'
        self.fields['phone'].label = 'Phone'
        self.fields['phone'].help_text = 'Please, use format +1234567890123'
        self.fields['buying_type'].label = 'Delivery type'
        self.fields['date'].label = 'Date of delivary'
        self.fields['date'].help_text = 'Delivery will be tomorrow'
        self.fields['address'].label = 'Address'
        self.fields['address'].help_text = 'Please, use your town'
        self.fields['comments'].label = 'Comments'

