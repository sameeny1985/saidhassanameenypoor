from django.db import models


class LinkItem(models.Model):

    class Category(models.TextChoices):

        ARTICLE = "article", "Articles"
        WEBSITE = "website", "Websites"
        VIDEO = "video", "Videos"
        YOUTUBE = "youtube", "YouTube Channels"
        TELEGRAM = "telegram", "Telegram Channels"

    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )

    title = models.CharField(
        max_length=180
    )

    description = models.TextField(
        blank=True
    )

    url = models.URLField(
        max_length=1000
    )

    # Optional external image URL (kept for compatibility)
    image_url = models.URLField(
        max_length=1000,
        blank=True
    )

    # Optional uploaded logo (preferred for display)
    logo = models.ImageField(
        upload_to="logos/",
        blank=True,
        null=True,
        help_text="Optional logo image (JPG/PNG). Shown small above each item."
    )

    is_published = models.BooleanField(
        default=True
    )

    sort_order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            "sort_order",
            "-created_at"
        ]

    def __str__(self):

        return (
            f"{self.get_category_display()}: "
            f"{self.title}"
        )

    @property
    def display_image(self):
        """Prefer uploaded logo, fall back to image_url."""
        if self.logo:
            return self.logo.url
        if self.image_url:
            return self.image_url
        return None
