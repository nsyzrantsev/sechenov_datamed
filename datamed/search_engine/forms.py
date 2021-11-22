from django import forms


class AddSearchForm(forms.Form):
    user_query = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите запрос...'
        }))
    articles_number = forms.IntegerField(
        min_value=0,
        max_value=10,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите число статей...'
        }))
