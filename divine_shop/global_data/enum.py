from django.db import models
from django.utils.translation import gettext_lazy as _

class ChatFileType(models.TextChoices):
    IMAGE = "image", _("Image")
    VIDEO = "video", _("Vidéo")
    AUDIO = "audio", _("Audio")

class SupportStatus(models.TextChoices):
    OPEN = "open", _("Ouvert")
    IN_PROGRESS = "in_progress", _("En cours")
    CLOSED = "closed", _("Fermé")

class SupportPriority(models.TextChoices):
    LOW = "low", _("Faible")
    MEDIUM = "medium", _("Moyen")
    HIGH = "high", _("Élevé")

class NotificationType(models.TextChoices):
    ORDER = "order", _("Commande")
    PAYMENT = "payment", _("Paiement")
    FORMATION = "formation", _("Formation")
    MESSAGE = "message", _("Message")
    SYSTEM = "system", _("Système")

class OrderStatus(models.TextChoices):
    PENDING = "pending", _("En attente")
    PAID = "paid", _("Payée")
    SHIPPED = "shipped", _("Expédiée")
    CANCELLED = "cancelled", _("Annulée")

class PaymentMethod(models.TextChoices):
    MTN = "mtn", _("MTN Mobile Money")
    ORANGE = "orange", _("Orange Money")

class PaymentStatus(models.TextChoices):
    PENDING = "pending", _("En attente")
    SUCCESS = "success", _("Réussi")
    FAILED = "failed", _("Échoué")

class UserRole(models.TextChoices):
    CLIENT = "client", _("Client")
    CREATRICE = "creatrice", _("Créatrice")
    FOURNISSEUR = "fournisseur", _("Fournisseur")

class ProductBadge(models.TextChoices):
    NEW = "new", _("Nouveau")
    FEATURED = "featured", _("Vedette")
    SALE = "sale", _("Promotion")
    SOLD_OUT = "sold_out", _("Épuisé")