from django import forms


class createnewuser(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label='Password',
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )
    email = forms.EmailField(
        label='Email',
        max_length=242,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

class loginuser(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label='Password',
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

# class createrole(forms.Form):
#     name = forms.CharField(
#         label='Name',
#         max_length=30,
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Role'})
#     )