from django import forms

from .models import LinkItem


class LinkItemForm(forms.ModelForm):

    class Meta:

        model = LinkItem

        fields = [
            "category",
            "title",
            "description",
            "url",
            "logo",
            "image_url",
            "is_published",
            "sort_order",
        ]

        widgets = {

            "category": forms.Select(
                attrs={
                    "class": "field"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "field",
                    "placeholder": "Title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "field",
                    "rows": 3,
                    "placeholder": "Short description (optional)"
                }
            ),

            "url": forms.URLInput(
                attrs={
                    "class": "field",
                    "placeholder": "https://..."
                }
            ),

            "image_url": forms.URLInput(
                attrs={
                    "class": "field",
                    "placeholder": "External image URL (optional, if no logo uploaded)"
                }
            ),

            "sort_order": forms.NumberInput(
                attrs={
                    "class": "field",
                    "min": 0
                }
            ),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["logo"].widget.attrs.update({
            "class": "field",
            "accept": "image/jpeg,image/png,image/webp"
        })
        self.fields["logo"].required = False
        self.fields["image_url"].required = False
        self.fields["description"].required = False
