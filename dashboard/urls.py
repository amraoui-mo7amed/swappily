from django.urls import path
from dashboard.views import dashboard, users, notifications, skills

app_name = "dash"

urlpatterns = [
    path("home/", dashboard.dash_home, name="dash_home"),
    path("users/", users.user_list, name="user_list"),
    path("users/<int:pk>/", users.user_details, name="user_details"),
    path("users/<int:pk>/delete/", users.user_delete, name="user_delete"),
    path("users/<int:pk>/approve/", users.user_approve, name="user_approve"),
    # Notifications
    path(
        "notifications/stream/",
        notifications.notifications_stream,
        name="notifications_stream",
    ),
    path(
        "notifications/unread-count/",
        notifications.get_unread_count,
        name="notifications_unread_count",
    ),
    path(
        "notifications/list/",
        notifications.get_notifications,
        name="notifications_list",
    ),
    path(
        "notifications/<int:notification_id>/read/",
        notifications.mark_as_read,
        name="notification_mark_read",
    ),
    path(
        "notifications/mark-all-read/",
        notifications.mark_all_as_read,
        name="notifications_mark_all_read",
    ),
    path(
        "notifications/<int:notification_id>/delete/",
        notifications.delete_notification,
        name="notification_delete",
    ),
    # Skills
    path("skills/", skills.skill_list, name="skill_list"),
    path("skills/create/", skills.skill_create, name="skill_create"),
    path("skills/<int:pk>/", skills.skill_detail, name="skill_detail"),
    path("skills/<int:pk>/update/", skills.skill_update, name="skill_update"),
    path("skills/<int:pk>/delete/", skills.skill_delete, name="skill_delete"),
    # Swap Requests
    path("swaps/", skills.swap_request_list, name="swap_request_list"),
    path("swaps/<int:pk>/", skills.swap_request_detail, name="swap_request_detail"),
    path(
        "skills/<int:pk>/request-swap/",
        skills.swap_request_create,
        name="swap_request_create",
    ),
    path(
        "swaps/<int:pk>/accept-form/",
        skills.swap_request_accept_form,
        name="swap_request_accept_form",
    ),
    path(
        "swaps/<int:pk>/accept/", skills.swap_request_accept, name="swap_request_accept"
    ),
    path(
        "swaps/<int:pk>/reject/", skills.swap_request_reject, name="swap_request_reject"
    ),
    path(
        "swaps/<int:pk>/cancel/", skills.swap_request_cancel, name="swap_request_cancel"
    ),
]
