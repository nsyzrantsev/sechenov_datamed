from django import forms


class AddSearchForm(forms.Form):
    user_query = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите запрос...'
            },
        ),
    )
