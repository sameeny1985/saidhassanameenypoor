from django import forms

from .models import LinkItem


class LinkItemForm(forms.ModelForm):

    clear_logo = forms.BooleanField(
        required=False,
        label="حذف لوگو",
        help_text="تیک بزنید تا لوگوی فعلی حذف شود",
    )

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

            # Plain FileInput — we handle clear ourselves with clear_logo
            "logo": forms.FileInput(
                attrs={
                    "class": "field",
                    "accept": "image/jpeg,image/png,image/webp"
                }
            ),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["logo"].required = False
        self.fields["image_url"].required = False
        self.fields["description"].required = False

        # Only show clear option when an existing logo is present
        if not (self.instance and self.instance.pk and self.instance.logo):
            self.fields["clear_logo"].widget = forms.HiddenInput()
            self.fields["clear_logo"].initial = False

    def save(self, commit=True):
        instance = super().save(commit=False)

        clear = self.cleaned_data.get("clear_logo")
        new_logo = self.cleaned_data.get("logo")

        # If user ticked "remove logo" and did not upload a replacement
        if clear and not new_logo:
            if instance.logo:
                instance.logo.delete(save=False)
            instance.logo = None

        if commit:
            instance.save()
            self.save_m2m()

        return instance
