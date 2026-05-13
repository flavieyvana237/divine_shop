from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from divine_shop.core.models import BaseModel


class SupportTicket(BaseModel):
    """Ticket de support client"""

    class Status(models.TextChoices):
        OPEN = "open", _("Ouvert")
        IN_PROGRESS = "in_progress", _("En cours")
        CLOSED = "closed", _("Fermé")

    class Priority(models.TextChoices):
        LOW = "low", _("Faible")
        MEDIUM = "medium", _("Moyen")
        HIGH = "high", _("Élevé")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("Client"),
    )
    subject = models.CharField(_("Sujet"), max_length=255)
    message = models.TextField(_("Message"))
    status = models.CharField(
        _("Statut"),
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )
    priority = models.CharField(
        _("Priorité"),
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    class Meta:
        verbose_name = _("Ticket support")
        verbose_name_plural = _("Tickets support")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} — {self.user.username}"