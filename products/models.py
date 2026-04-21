from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Category(models.Model):
    """Catégorie d'accessoires en perles"""

    name = models.CharField(_("Nom"), max_length=100, unique=True)
    slug = models.SlugField(_("Slug"), max_length=120, unique=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Produit (accessoire en perles)"""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Catégorie"),
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


class ProductImage(models.Model):
    """Images multiples pour un même produit"""

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
