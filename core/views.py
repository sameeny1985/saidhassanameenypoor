import secrets
import logging

from urllib.parse import urlencode

import requests

from django.conf import settings

from django.contrib import messages

from django.http import (
    HttpResponse,
    HttpResponseForbidden
)

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from django.utils import timezone
from django.db import DatabaseError, ProgrammingError

from .forms import LinkItemForm

from .models import LinkItem

logger = logging.getLogger(__name__)

GOOGLE_AUTH_URL = (
    "https://accounts.google.com/o/oauth2/v2/auth"
)

GOOGLE_TOKEN_URL = (
    "https://oauth2.googleapis.com/token"
)

GOOGLE_USERINFO_URL = (
    "https://openidconnect.googleapis.com/v1/userinfo"
)


def _empty_groups():
    return {
        "article": [],
        "website": [],
        "video": [],
        "youtube": [],
        "telegram": [],
    }


def home(request):
    groups = _empty_groups()

    try:
        for key in groups:
            groups[key] = list(
                LinkItem.objects.filter(
                    category=key,
                    is_published=True
                )
            )
    except (DatabaseError, ProgrammingError) as exc:
        # Schema not migrated yet or DB issue — still show page
        logger.exception("Homepage DB error (safe fallback): %s", exc)

    return render(
        request,
        "core/home.html",
        {"groups": groups}
    )


def health(request):
    return HttpResponse("ok")


def _is_admin(request):
    return request.session.get("portfolio_admin") is True


def google_login(request):
    if not all([
        settings.ADMIN_EMAIL,
        settings.GOOGLE_CLIENT_ID,
        settings.GOOGLE_CLIENT_SECRET
    ]):
        return HttpResponse(
            "Google login is not configured. "
            "Set ADMIN_EMAIL, GOOGLE_CLIENT_ID "
            "and GOOGLE_CLIENT_SECRET in Render.",
            status=503
        )

    state = secrets.token_urlsafe(32)
    request.session["google_oauth_state"] = state

    callback = settings.SITE_URL + "/auth/google/callback/"

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": callback,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "prompt": "select_account",
    }

    return redirect(GOOGLE_AUTH_URL + "?" + urlencode(params))


def google_callback(request):
    expected_state = request.session.pop("google_oauth_state", None)

    if not expected_state or request.GET.get("state") != expected_state:
        return HttpResponseForbidden(
            "Invalid OAuth state. Please try again."
        )

    code = request.GET.get("code")
    if not code:
        return HttpResponse("Authorization failed (no code).", status=400)

    callback = settings.SITE_URL + "/auth/google/callback/"

    try:
        token_response = requests.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": callback,
                "grant_type": "authorization_code",
            },
            timeout=15
        )
        token_response.raise_for_status()
        tokens = token_response.json()
        access_token = tokens["access_token"]

        user_response = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=15
        )
        user_response.raise_for_status()
        user = user_response.json()

    except (requests.RequestException, KeyError, ValueError):
        return HttpResponse(
            "Could not verify your Google account.",
            status=502
        )

    email = str(user.get("email", "")).strip().lower()

    if (
        user.get("email_verified") is not True
        or email != settings.ADMIN_EMAIL
    ):
        request.session.flush()
        return HttpResponseForbidden(
            "This Google account is not authorized."
        )

    request.session.cycle_key()
    request.session["portfolio_admin"] = True
    request.session["portfolio_admin_email"] = email

    return redirect("admin_dashboard")


def admin_logout(request):
    request.session.flush()
    return redirect("home")


def admin_dashboard(request):
    if not _is_admin(request):
        return redirect("google_login")

    try:
        items = LinkItem.objects.all().order_by(
            "category", "sort_order", "-created_at"
        )
    except (DatabaseError, ProgrammingError):
        items = []

    return render(
        request,
        "core/admin_dashboard.html",
        {"items": items}
    )


def item_create(request):
    if not _is_admin(request):
        return redirect("google_login")

    form = LinkItemForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Item added successfully.")
        return redirect("admin_dashboard")

    return render(
        request,
        "core/item_form.html",
        {"form": form, "heading": "Add a new link"}
    )


def item_edit(request, pk):
    if not _is_admin(request):
        return redirect("google_login")

    item = get_object_or_404(LinkItem, pk=pk)

    form = LinkItemForm(
        request.POST or None,
        request.FILES or None,
        instance=item
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Changes saved.")
        return redirect("admin_dashboard")

    return render(
        request,
        "core/item_form.html",
        {"form": form, "heading": "Edit link"}
    )


def item_delete(request, pk):
    if not _is_admin(request):
        return redirect("google_login")

    item = get_object_or_404(LinkItem, pk=pk)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Item deleted.")
        return redirect("admin_dashboard")

    return render(
        request,
        "core/confirm_delete.html",
        {"item": item}
    )


def sitemap_xml(request):
    site_url = settings.SITE_URL.rstrip("/")
    lastmod = timezone.localdate().isoformat()

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{site_url}/</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
"""
    return HttpResponse(xml, content_type="application/xml")


def robots_txt(request):
    site_url = settings.SITE_URL.rstrip("/")
    content = f"""User-agent: *
Allow: /

Disallow: /admin/
Disallow: /auth/

Sitemap: {site_url}/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")
