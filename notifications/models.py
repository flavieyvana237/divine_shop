

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from divine_shop.core.models import BaseModel


class Notification(BaseModel):
    """Notification utilisateur"""

    class Type(models.TextChoices):
        ORDER = "order", _("Commande")
        PAYMENT = "payment", _("Paiement")
        FORMATION = "formation", _("Formation")
        MESSAGE = "message", _("Message")
        SYSTEM = "system", _("Système")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Destinataire"),
    )
    type = models.CharField(
        _("Type"),
        max_length=20,
        choices=Type.choices,
        default=Type.SYSTEM,
    )
    message = models.TextField(_("Message"))
    is_read = models.BooleanField(_("Lu"), default=False)
    link = models.CharField(
        _("Lien"),
        max_length=255,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} — {self.type}"