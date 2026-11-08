from django import forms

from .models import LinkItem


class LinkItemForm(forms.ModelForm):

    clear_logo = forms.BooleanField(
        required=False,
        label="Delete logo",
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
            "category": forms.Select(attrs={"class": "field"}),
            "title": forms.TextInput(attrs={
                "class": "field",
                "placeholder": "Title",
            }),
            "description": forms.Textarea(attrs={
                "class": "field",
                "rows": 3,
                "placeholder": "Short description (optional)",
            }),
            "url": forms.URLInput(attrs={
                "class": "field",
                "placeholder": "https://...",
            }),
            # Plain FileInput — no Django "Currently / Clear" double UI
            "logo": forms.FileInput(attrs={
                "class": "field",
                "accept": "image/jpeg,image/png,image/webp",
            }),
            "image_url": forms.URLInput(attrs={
                "class": "field",
                "placeholder": "External image URL (optional)",
            }),
            "sort_order": forms.NumberInput(attrs={
                "class": "field",
                "min": 0,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["logo"].required = False
        self.fields["image_url"].required = False
        self.fields["description"].required = False

        has_logo = bool(
            self.instance
            and self.instance.pk
            and self.instance.logo
            and getattr(self.instance.logo, "name", "")
        )
        if not has_logo:
            self.fields.pop("clear_logo", None)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get("clear_logo"):
            if instance.logo:
                try:
                    instance.logo.delete(save=False)
                except Exception:
                    pass
            instance.logo = None

        if commit:
            instance.save()
            self.save_m2m()

        return instance
