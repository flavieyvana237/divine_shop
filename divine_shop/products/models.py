from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from divine_shop.core.models import BaseModel
from global_data.enum import ProductBadge


class Category(BaseModel):
    """Catégorie d'accessoires en perles"""

    name = models.CharField(_("Nom"), max_length=100, unique=True)
    slug = models.SlugField(_("Slug"), max_length=120, unique=True)
    description = models.TextField(_("Description"), blank=True, default="")
    image = models.ImageField(
        _("Image"),
        upload_to="categories/",
        blank=True,
        null=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="categories",
        verbose_name=_("Créée par"),
    )

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(BaseModel):
    """Produit (accessoire en perles)"""

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
        null=True,
        blank=True,
    )
    name = models.CharField(_("Nom du produit"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=250, unique=True)
    description = models.TextField(_("Description détaillée"))
    price = models.DecimalField(_("Prix"), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_("Stock disponible"), default=0)
    is_available = models.BooleanField(_("Disponible"), default=True)

    # ← Nouveaux champs
    is_featured = models.BooleanField(_("Produit vedette"), default=False)
    is_new = models.BooleanField(_("Nouveau produit"), default=False)

    class Meta:
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.price} FCFA"

    def get_main_image(self):
        main = self.images.filter(is_main=True).first()
        return main or self.images.first()

    def is_in_stock(self):
        return self.stock > 0 and self.is_available

    def get_active_promotion(self):
        """Retourne la promotion active si elle existe"""
        now = timezone.now()
        return self.promotions.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now,
        ).first()

    def get_promo_price(self):
        """Prix après réduction"""
        promo = self.get_active_promotion()
        if promo:
            reduction = (self.price * promo.discount_percentage) / 100
            return round(self.price - reduction, 2)
        return self.price

    def get_discount_percentage(self):
        """Pourcentage de réduction"""
        promo = self.get_active_promotion()
        return promo.discount_percentage if promo else 0

    def is_on_sale(self):
        """Produit en promotion ?"""
        return self.get_active_promotion() is not None

    def get_badge(self):
        """Retourne le badge à afficher sur la carte produit"""
        if self.is_on_sale():
            return ProductBadge.SALE
        if self.is_new:
            return ProductBadge.NEW
        if self.is_featured:
            return ProductBadge.FEATURED
        if not self.is_in_stock():
            return ProductBadge.SOLD_OUT
        return None


class ProductImage(BaseModel):
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


class Promotion(BaseModel):
    """Promotion avec période et réduction automatique"""

    name = models.CharField(_("Nom de la promotion"), max_length=255)
    description = models.TextField(_("Description"), blank=True, default="")
    discount_percentage = models.PositiveIntegerField(_("Réduction (%)"))
    start_date = models.DateTimeField(_("Date de début"))
    end_date = models.DateTimeField(_("Date de fin"))
    products = models.ManyToManyField(
        Product,
        related_name="promotions",
        verbose_name=_("Produits concernés"),
        blank=True,
    )
    is_active = models.BooleanField(_("Active"), default=True)
    banner_image = models.ImageField(
        _("Image bannière"),
        upload_to="promotions/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def is_currently_active(self):
        """Vérifie si la promotion est active maintenant"""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def time_remaining(self):
        """Temps restant avant la fin de la promotion"""
        now = timezone.now()
        if self.end_date > now:
            return self.end_date - now
        return None