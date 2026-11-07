
import logging

from django.db import DatabaseError
from django.shortcuts import render

from .models import LinkItem

logger = logging.getLogger(__name__)


def home(request):

    groups = {
        "article": [],
        "website": [],
        "video": [],
        "telegram": [],
    }

    try:
        items = list(
            LinkItem.objects.filter(
                is_published=True
            ).order_by(
                "sort_order",
                "-created_at"
            )
        )

        for item in items:
            if item.category in groups:
                groups[item.category].append(item)

    except DatabaseError:
        logger.exception(
            "Database error while loading homepage"
        )

    return render(
        request,
        "core/home.html",
        {
            "groups": groups
        }
    )
