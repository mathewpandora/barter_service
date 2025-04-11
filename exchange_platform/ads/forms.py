from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок объявления',
            'description': 'Описание товара',
            'image': 'Изображение',
            'category': 'Категория товара',
            'condition': 'Состояние товара (новый/б/у)',
        }


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']

    ad_sender = forms.ModelChoiceField(
        queryset=Ad.objects.none(),
        required=True,
        label="Выберите объявление для обмена"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)

