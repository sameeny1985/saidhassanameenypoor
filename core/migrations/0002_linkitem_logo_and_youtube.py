from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [

        migrations.AddField(
            model_name="linkitem",
            name="logo",
            field=models.ImageField(
                blank=True,
                help_text="Optional logo image (JPG/PNG). Shown small above each item.",
                null=True,
                upload_to="logos/",
            ),
        ),

        migrations.AlterField(
            model_name="linkitem",
            name="category",
            field=models.CharField(
                choices=[
                    ("article", "Articles"),
                    ("website", "Websites"),
                    ("video", "Videos"),
                    ("youtube", "YouTube Channels"),
                    ("telegram", "Telegram Channels"),
                ],
                max_length=20,
            ),
        ),

    ]
