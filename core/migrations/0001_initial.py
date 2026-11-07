from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [

        migrations.CreateModel(

            name="LinkItem",

            fields=[

                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID"
                    )
                ),

                (
                    "category",
                    models.CharField(
                        choices=[
                            ("article", "Articles"),
                            ("website", "Websites"),
                            ("video", "Videos"),
                            ("telegram", "Telegram Channels"),
                        ],
                        max_length=20
                    )
                ),

                (
                    "title",
                    models.CharField(max_length=180)
                ),

                (
                    "description",
                    models.TextField(blank=True)
                ),

                (
                    "url",
                    models.URLField(max_length=1000)
                ),

                (
                    "image_url",
                    models.URLField(
                        blank=True,
                        max_length=1000
                    )
                ),

                (
                    "is_published",
                    models.BooleanField(default=True)
                ),

                (
                    "sort_order",
                    models.PositiveIntegerField(default=0)
                ),

                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True)
                ),

                (
                    "updated_at",
                    models.DateTimeField(auto_now=True)
                ),

            ],

            options={
                "ordering": [
                    "sort_order",
                    "-created_at"
                ]
            },

        ),

    ]
