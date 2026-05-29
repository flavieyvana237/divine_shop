from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models import TextChoices
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from divine_shop.core.models import BaseModel
import uuid
from django.conf import settings

from divine_shop.global_data.enum import UserRole


class User(AbstractUser):
    """
    Custom user model for Divine Shop.
    Roles: client, créatrice, fournisseur
    """

    name = CharField(_("Nom complet"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    role = models.CharField(
        _("Rôle"),
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CLIENT,  # ← tout le monde commence client
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
        return self.role == UserRole.CREATRICE

    def is_fournisseur(self) -> bool:
        return self.role == UserRole.FOURNISSEUR

    def is_client(self) -> bool:
        return self.role == UserRole.CLIENT

class Testimonial(BaseModel):
    """Témoignages et avis des clients de Divine Shop"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials",
        verbose_name=_("Client (Optionnel)")
    )
    client_name = models.CharField(_("Nom du client"), max_length=100)
    client_title = models.CharField(_("Titre / Rôle"), max_length=100, blank=True, default="Cliente vérifiée")
    avatar = models.ImageField(_("Avatar"), upload_to="avatars/", blank=True, null=True)
    comment = models.TextField(_("Commentaire / Avis"))
    rating = models.PositiveIntegerField(_("Note (Étoiles)"), default=5)
    is_approved = models.BooleanField(_("Approuvé pour l'affichage"), default=False)

    class Meta:
        verbose_name = _("Témoignage")
        verbose_name_plural = _("Témoignages")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Avis de {self.client_name} - {self.rating}★"