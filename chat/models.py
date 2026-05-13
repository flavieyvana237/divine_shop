

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from divine_shop.core.models import BaseModel


class Message(BaseModel):
    """Message dans un groupe privé"""

    class FileType(models.TextChoices):
        IMAGE = "image", _("Image")
        VIDEO = "video", _("Vidéo")
        AUDIO = "audio", _("Audio")

    group = models.ForeignKey(
        "formations.Group",
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("Groupe"),
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="group_messages",
        verbose_name=_("Expéditeur"),
    )
    content = models.TextField(_("Message"), blank=True, default="")
    file = models.FileField(
        _("Fichier"),
        upload_to="chat/files/",
        blank=True,
        null=True,
    )
    file_type = models.CharField(
        _("Type de fichier"),
        max_length=10,
        choices=FileType.choices,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = _("Message groupe")
        verbose_name_plural = _("Messages groupe")
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username} → {self.group.name}"


class PrivateMessage(BaseModel):
    """Message privé entre deux utilisateurs"""
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name=_("Expéditeur"),
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
        verbose_name=_("Destinataire"),
    )
    content = models.TextField(_("Message"), blank=True, default="")
    file = models.FileField(
        _("Fichier"),
        upload_to="chat/private/",
        blank=True,
        null=True,
    )
    is_read = models.BooleanField(_("Lu"), default=False)

    class Meta:
        verbose_name = _("Message privé")
        verbose_name_plural = _("Messages privés")
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"