from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок объявления',
            'description': 'Описание товара',
            'image_url': 'URL изображения',
            'category': 'Категория товара',
            'condition': 'Состояние товара (новый/б/у)',
        }


from django import forms
from .models import ExchangeProposal, Ad


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']  # Только отправитель и комментарий

    # Переопределим поле ad_sender, чтобы только объявления текущего пользователя были доступны
    ad_sender = forms.ModelChoiceField(
        queryset=Ad.objects.none(),  # Изначально пустой, будет обновляться в __init__
        required=True,
        label="Выберите объявление для обмена"
    )

    def __init__(self, *args, **kwargs):
        # Передаем пользователя через аргументы
        user = kwargs.pop('user', None)  # Получаем пользователя, переданного в аргументах

        super().__init__(*args, **kwargs)

        # Ограничиваем выбор только объявлениями текущего пользователя
        if user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)

