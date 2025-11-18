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

MAX_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_CONTENT_TYPES = ('image/jpeg', 'image/png')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Проставляем Bootstrap-классы для всех полей формы
        for name, field in self.fields.items():
            widget = field.widget
            existing_classes = widget.attrs.get('class', '')
            if isinstance(widget, forms.CheckboxInput):
                # Булевые поля — отдельный класс
                classes = f"{existing_classes} form-check-input".strip()
            else:
                classes = f"{existing_classes} form-control".strip()
            widget.attrs['class'] = classes

    def _validate_forbidden_words(self, value: str, field_label: str) -> str:
        if not value:
            return value
        lowered = value.lower()
        for word in FORBIDDEN_WORDS:
            if word in lowered:
                raise forms.ValidationError(
                    f'Слово "{word}" запрещено для использования в поле "{field_label}".'
                )
        return value

    def clean_name(self) -> str:
        name = self.cleaned_data.get('name', '')
        return self._validate_forbidden_words(name, 'Название')

    def clean_description(self) -> str:
        description = self.cleaned_data.get('description', '')
        return self._validate_forbidden_words(description, 'Описание')

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена продукта не может быть отрицательной.')
        return price

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
