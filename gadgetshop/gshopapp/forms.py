from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from gshopapp.models import DELIVERY_CHOICES


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    password_check = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email'
        ]


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'
        self.fields['password_check'].label = 'Repeat password'
        self.fields['first_name'].label = 'First name'
        self.fields['last_name'].label = 'Last name'
        self.fields['email'].label = 'Email'


    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Please, use another username!')
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if password != password_check:
            raise forms.ValidationError('Password are different!')
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Please, use another email!')



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


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


    def clean(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if len(user) > 0:
            user = user.first()
            password = self.cleaned_data['password']
            if user.check_password(password):
                return
        raise forms.ValidationError("Invalid username or password!")