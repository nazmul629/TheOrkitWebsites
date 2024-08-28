from django import forms
from .models import Account,UserProfile
from django import forms

class RegistrationForm(forms.ModelForm):
 
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))
         

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = "Enter Email"
        
        # Apply the 'form-control' class to all fields
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleand_data =  super(RegistrationForm,self).clean()
        password = cleand_data.get('password')
        confirm_password = cleand_data.get('confirm_password')
        if password !=confirm_password:
            raise forms.ValidationError(
                "Password Does not match"
            )

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number')


    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_pic  = forms.ImageField(required=False,error_messages={'invalid':("Image file only")},widget=forms.FileInput)
    class Meta :
        model = UserProfile
        fields = ('address_line_1','address_line_2', 'city', 'state','country', 'profile_pic')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'  