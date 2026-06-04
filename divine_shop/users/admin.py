from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import NewsletterUser, Testimonial, User

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

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    # Les colonnes qui vont s'afficher dans la liste des témoignages
    list_display = ["client_name", "rating", "client_title", "is_approved", "created_at"]
    
    # Les filtres sur le côté droit pour trier rapidement
    list_filter = ["is_approved", "rating", "created_at"]
    
    # La barre de recherche pour retrouver un avis par le nom du client ou son texte
    search_fields = ["client_name", "comment", "client_title"]
    
    # Permet de cocher/décocher "Approuvé" directement depuis la liste sans ouvrir le témoignage
    list_editable = ["is_approved"]
    
    # Rend les dates de création visibles mais non modifiables
    readonly_fields = ["created_at", "updated_at"]


@admin.register(NewsletterUser)  
class NewsletterUserAdmin(admin.ModelAdmin):
    
    # Les colonnes visibles dans la liste
    list_display = ["email", "is_active", "has_received_welcome_coupon", "created_at"]
    
    # Filtres rapides sur la droite
    list_filter = ["is_active", "has_received_welcome_coupon", "created_at"]
    
    # Barre de recherche pour chercher un mail précis
    search_fields = ["email"]
    
    # Actions rapides pour activer/désactiver un abonné depuis la liste
    list_editable = ["is_active"]