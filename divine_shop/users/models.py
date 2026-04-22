from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models import TextChoices
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model for Divine Shop.
    Roles: client, créatrice, fournisseur
    """

    class Role(TextChoices):
        CLIENT = "client", _("Client")
        CREATRICE = "creatrice", _("Créatrice")
        FOURNISSEUR = "fournisseur", _("Fournisseur")

    name = CharField(_("Nom complet"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    role = models.CharField(
        _("Rôle"),
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,  # ← tout le monde commence client
    )
    phone = models.CharField(
        _("Téléphone"),
        max_length=20,
        blank=True,
        default="",
    )
    profile_image = models.ImageField(
        _("Photo de profil"),
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.username})

    def is_creatrice(self) -> bool:
        return self.role == self.Role.CREATRICE

    def is_fournisseur(self) -> bool:
        return self.role == self.Role.FOURNISSEUR

    def is_client(self) -> bool:
        return self.role == self.Role.CLIENT
