from functools import lru_cache
from django.conf import settings
from django.utils.translation import gettext_lazy as _, get_language


@lru_cache(maxsize=1)
def _get_cached_site_settings():
    """
    Cached version of site settings.
    This is cached at module level to avoid recreating on every request.
    """
    return {
        "name": _("Swappily"),
        "ar_name": "سوابيلي",
        "tagline": _("AI-Powered Landing Pages"),
        "logo": None,
        "favicon": None,
        "contact_email": "info@swappily.com",
        "phone": "+213 555 000 000",
        "social": {
            "facebook": "https://facebook.com/snapstore",
            "twitter": "https://twitter.com/snapstore",
            "instagram": "https://instagram.com/snapstore",
        },
        "seo": {
            "description": _("Start Learning By Exchanging Skills"),
            "keywords": _("swappily, exchange skills, learn, exchange"),
        },
        "branding": {
            "primary_color": "#0d6efd",
            "secondary_color": "#6c757d",
            "accent_color": "#ffc107",
            "success_color": "#198754",
            "danger_color": "#dc3545",
            "dark_color": "#212529",
            "light_color": "#f8f9fa",
        },
    }


def site_settings(request):
    """
    Returns global site configuration and branding details.
    Uses cached settings to improve performance.
    """
    return {
        "site_config": _get_cached_site_settings()
    }
    }
