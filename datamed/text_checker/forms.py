from django import forms


class AddTextareaForm(forms.Form):
    user_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Введите текст...'
            }
        )
    )
