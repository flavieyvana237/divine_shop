# Create your models here.

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from divine_shop.core.models import BaseModel


class Cart(BaseModel):
    """Panier d'un utilisateur — un seul panier par user"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name=_("Utilisateur"),
    )

    class Meta:
        verbose_name = _("Panier")
        verbose_name_plural = _("Paniers")

    def __str__(self):
        return f"Panier de {self.user.username}"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())


class CartItem(BaseModel):
    """Produit dans le panier"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Panier"),
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        verbose_name=_("Produit"),
    )
    quantity = models.PositiveIntegerField(_("Quantité"), default=1)

    class Meta:
        verbose_name = _("Article du panier")
        verbose_name_plural = _("Articles du panier")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        return self.product.price * self.quantity


class Order(BaseModel):
    """Commande validée"""

    class Status(models.TextChoices):
        PENDING = "pending", _("En attente")
        PAID = "paid", _("Payée")
        SHIPPED = "shipped", _("Expédiée")
        CANCELLED = "cancelled", _("Annulée")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("Client"),
    )
    total_amount = models.DecimalField(
        _("Montant total"),
        max_digits=10,
        decimal_places=2,
    )
    status = models.CharField(
        _("Statut"),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    delivery_address = models.TextField(_("Adresse de livraison"))

    class Meta:
        verbose_name = _("Commande")
        verbose_name_plural = _("Commandes")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Commande {self.id} — {self.user.username}"


class OrderItem(BaseModel):
    """Produit dans une commande"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Commande"),
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        verbose_name=_("Produit"),
    )
    quantity = models.PositiveIntegerField(_("Quantité"))
    price = models.DecimalField(
        _("Prix unitaire"),
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        verbose_name = _("Article commandé")
        verbose_name_plural = _("Articles commandés")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        return self.price * self.quantity


class Payment(BaseModel):
    """Paiement lié à une commande"""

    class Method(models.TextChoices):
        MTN = "mtn", _("MTN Mobile Money")
        ORANGE = "orange", _("Orange Money")

    class Status(models.TextChoices):
        PENDING = "pending", _("En attente")
        SUCCESS = "success", _("Réussi")
        FAILED = "failed", _("Échoué")

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
        verbose_name=_("Commande"),
    )
    amount = models.DecimalField(_("Montant"), max_digits=10, decimal_places=2)
    method = models.CharField(
        _("Méthode"),
        max_length=10,
        choices=Method.choices,
    )
    status = models.CharField(
        _("Statut"),
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    transaction_ref = models.CharField(
        _("Référence transaction"),
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Paiement")
        verbose_name_plural = _("Paiements")

    def __str__(self):
        return f"Paiement {self.transaction_ref} — {self.status}"