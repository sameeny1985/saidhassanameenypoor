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

    # Google authentication

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

    # Admin panel

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
