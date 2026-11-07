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
                    "rows": 4,
                    "placeholder": "Description"
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
                    "placeholder": "Image URL (optional)"
                }
            ),

            "sort_order": forms.NumberInput(
                attrs={
                    "class": "field",
                    "min": 0
                }
            ),

        }
