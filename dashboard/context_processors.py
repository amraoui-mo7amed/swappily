from functools import lru_cache
from django.utils.translation import gettext_lazy as _


@lru_cache(maxsize=1)
def _get_cached_dashboard_menu():
    """
    Cached version of dashboard menu.
    This is cached at module level to avoid recreating on every request.
    """
    return [
        {
            "title": _("Dashboard"),
            "icon": "fas fa-th-large",
            "url_name": "dash:dash_home",
            "admin_only": False,
        },
        {
            "title": _("Skills"),
            "icon": "fas fa-lightbulb",
            "url_name": "dash:skill_list",
            "admin_only": False,
        },
        {
            "title": _("Swap Requests"),
            "icon": "fas fa-exchange-alt",
            "url_name": "dash:swap_request_list",
            "admin_only": False,
        },
        {
            "title": _("Users"),
            "icon": "fas fa-users",
            "url_name": "dash:user_list",
            "admin_only": True,
        },
    ]


def dashboard_sidebar(request):
    """
    Returns the dashboard menu items with RBAC flags.
    Uses cached menu to improve performance.
    """
    return {"dashboard_menu": _get_cached_dashboard_menu()}
