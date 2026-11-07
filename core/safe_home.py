
import logging

from django.http import HttpResponse
from django.utils.html import escape

from . import views

logger = logging.getLogger(__name__)


def safe_home(request):
    try:
        response = views.home(request)

        if response.status_code >= 500:
            logger.error(
                "Homepage returned HTTP %s",
                response.status_code
            )
            return homepage_fallback()

        return response

    except Exception as exc:
        logger.exception("HOMEPAGE CRASH")
        return homepage_fallback(str(exc))


def homepage_fallback(error=""):
    message = escape(str(error)) if error else ""

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
        <title>Said Hassanameenypoor</title>
        <style>
            body {{
                margin: 0;
                background: #101827;
                color: white;
                font-family: Arial, sans-serif;
                display: grid;
                place-items: center;
                min-height: 100vh;
                text-align: center;
            }}
            main {{
                max-width: 650px;
                padding: 30px;
            }}
            h1 {{ font-size: 32px; }}
            p {{ color: #aab7ca; line-height: 1.8; }}
        </style>
    </head>
    <body>
        <main>
            <h1>Said Hassanameenypoor</h1>
            <p>Personal Website</p>
            <p>The homepage is temporarily unavailable.</p>
            <p>{message}</p>
        </main>
    </body>
    </html>
    """

    return HttpResponse(html, status=200)
