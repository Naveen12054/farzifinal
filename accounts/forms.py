from django import forms
from .models import CustomUser
# from .validators import allow_only_images_validator


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control form-control-lg",
            "id":"pass",
            'placeholder': 'Enter Password'}
        ))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control form-control-lg",
            "id":"cpass",
            'placeholder': 'Confirm Password'}
        ))
    
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "id":"name",
                'placeholder': 'Enter Name'
            }
        )
    )
    phone = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-lg",
                "id":"phone",
                'placeholder': 'Enter Phone'
            }
        )
    )
    email=forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg",
                "id":"mail",
                'placeholder': 'Enter Email',
                }
        )
    )




    class Meta:
        model = CustomUser
        fields = ['name','email', 'phone','password']
        
      
        

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
