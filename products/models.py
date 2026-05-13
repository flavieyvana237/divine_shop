import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Catégorie d'accessoires en perles"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Nom"), max_length=100, unique=True)
    slug = models.SlugField(_("Slug"), max_length=120, unique=True)
    description = models.TextField(_("Description"), blank=True, default="")
    image= models.ImageField(_("Image de la catégorie"), upload_to="categories/", blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="categories",
        verbose_name=_("Créée par"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Produit (accessoire en perles)"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Catégorie"),
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Vendeur"),
        null=True,  # ← ajoute ces deux lignes
        blank=True,  # ← temporairement
    )
    name = models.CharField(_("Nom du produit"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=250, unique=True)
    description = models.TextField(_("Description détaillée"))
    price = models.DecimalField(_("Prix"), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_("Stock disponible"), default=0)
    is_available = models.BooleanField(_("Disponible"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.price} FCFA"

    def get_main_image(self):
        """Retourne l'image principale du produit"""
        main = self.images.filter(is_main=True).first()
        return main or self.images.first()

    def is_in_stock(self):
        """Vérifie si le produit est en stock"""
        return self.stock > 0 and self.is_available


class ProductImage(models.Model):
    """Images multiples pour un même produit"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Produit"),
    )
    image = models.ImageField(_("Image"), upload_to="products/")
    is_main = models.BooleanField(_("Image principale"), default=False)
    order = models.PositiveIntegerField(_("Ordre d'affichage"), default=0)

    class Meta:
        verbose_name = _("Image du produit")
        verbose_name_plural = _("Images du produit")
        ordering = ["order"]

    def __str__(self):
        return f"Image de {self.product.name}"
