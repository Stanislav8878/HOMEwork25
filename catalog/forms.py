# catalog/forms.py
from django import forms

from .models import Product, Category


FORBIDDEN_WORDS = (
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
)

ALLOWED_IMAGE_CONTENT_TYPES = (
    'image/jpeg',
    'image/png',
)

MAX_IMAGE_SIZE_MB = 2


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        lowered = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in lowered:
                raise forms.ValidationError(
                    f'Слово «{word}» запрещено в названии товара.'
                )
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '') or ''
        lowered = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in lowered:
                raise forms.ValidationError(
                    f'Слово «{word}» запрещено в описании товара.'
                )
        return description

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name') or ''
        description = cleaned_data.get('description') or ''

        if name and description and name.strip() == description.strip():
            raise forms.ValidationError(
                'Название и описание товара не должны совпадать.'
            )

        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image

        # Проверяем тип файла
        content_type = getattr(image, 'content_type', None)
        if content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
            raise forms.ValidationError(
                'Разрешены только изображения в форматах JPEG или PNG.'
            )

        # Проверяем размер файла
        max_size_bytes = MAX_IMAGE_SIZE_MB * 1024 * 1024
        if image.size > max_size_bytes:
            raise forms.ValidationError(
                f'Размер файла не должен превышать {MAX_IMAGE_SIZE_MB} МБ.'
            )

        return image
