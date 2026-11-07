from django.urls import path

from core import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "health/",
        views.health,
        name="health"
    ),

    path(
        "robots.txt",
        views.robots_txt,
        name="robots"
    ),

    path(
        "sitemap.xml",
        views.sitemap_xml,
        name="sitemap"
    ),

    path(
        "auth/google/",
        views.google_login,
        name="google_login"
    ),

    path(
        "auth/google/callback/",
        views.google_callback,
        name="google_callback"
    ),

    path(
        "auth/logout/",
        views.admin_logout,
        name="admin_logout"
    ),

    path(
        "admin/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "admin/add/",
        views.item_create,
        name="item_create"
    ),

    path(
        "admin/<int:pk>/edit/",
        views.item_edit,
        name="item_edit"
    ),

    path(
        "admin/<int:pk>/delete/",
        views.item_delete,
        name="item_delete"
    ),

]
