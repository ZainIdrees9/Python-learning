from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSignupForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password'
            }
        ),
        label='Password'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password'
            }
        ),
        label='Confirm Password'
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'role',
        ]

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter username'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email'
                }
            ),

            'role': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Admin should not be created through public signup
        self.fields['role'].choices = [
            ('MANAGER', 'Manager'),
            ('SALESMAN', 'Salesman'),
        ]

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username is already registered.'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email is already registered.'
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    'Passwords do not match.'
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Securely hash the password
        user.set_password(
            self.cleaned_data['password']
        )

        if commit:
            user.save()

        return user