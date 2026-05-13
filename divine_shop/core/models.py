import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Classe de base abstraite.
    Tous les modèles du projet héritent de cette classe.
    Contient les champs communs : id (UUID), created_at, updated_at.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # ← pas de table créée pour BaseModel