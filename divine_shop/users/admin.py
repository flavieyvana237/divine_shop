from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Informations personnelles"),
            {"fields": ("name", "email", "phone", "profile_image")},
        ),
        (_("Rôle"), {"fields": ("role",)}),  # ← nouveau
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Dates importantes"), {"fields": ("last_login", "date_joined")}),
    )

    # Ce que la créatrice verra dans la liste des utilisateurs
    list_display = ["username", "name", "email", "role", "is_superuser"]

    # Filtrer par rôle dans l'admin
    list_filter = ["role", "is_superuser", "is_active"]

    search_fields = ["username", "name", "email"]
