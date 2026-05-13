# Create your models here.
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from divine_shop.core.models import BaseModel


class Formation(BaseModel):
    """Formation en ligne"""
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="formations",
        verbose_name=_("Créatrice"),
    )
    title = models.CharField(_("Titre"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=280, unique=True)
    description = models.TextField(_("Description"))
    price = models.DecimalField(_("Prix"), max_digits=10, decimal_places=2)
    image = models.ImageField(
        _("Image"),
        upload_to="formations/",
        blank=True,
        null=True,
    )
    is_available = models.BooleanField(_("Disponible"), default=True)

    class Meta:
        verbose_name = _("Formation")
        verbose_name_plural = _("Formations")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Group(BaseModel):
    """Groupe privé lié à une formation"""
    formation = models.OneToOneField(
        Formation,
        on_delete=models.CASCADE,
        related_name="group",
        verbose_name=_("Formation"),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="groups_created",
        verbose_name=_("Créé par"),
    )
    name = models.CharField(_("Nom"), max_length=255)
    description = models.TextField(_("Description"), blank=True, default="")

    class Meta:
        verbose_name = _("Groupe")
        verbose_name_plural = _("Groupes")

    def __str__(self):
        return self.name


class GroupMember(BaseModel):
    """Membre d'un groupe privé"""
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name=_("Groupe"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="group_memberships",
        verbose_name=_("Membre"),
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Membre du groupe")
        verbose_name_plural = _("Membres du groupe")
        unique_together = ["group", "user"]

    def __str__(self):
        return f"{self.user.username} — {self.group.name}"