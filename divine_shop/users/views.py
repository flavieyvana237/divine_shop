from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from divine_shop.users.models import User

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import NewsletterUser

if TYPE_CHECKING:
    from django.db.models import QuerySet


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


#la view pour s'inscrire à la newsletter, qui reçoit une requete POST avec l'email, et qui retourne un JsonResponse avec le message de succès ou d'erreur
@csrf_protect
def newsletter_subscribe(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip().lower()
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": _("Données invalides.")}, status=400)

        if not email:
            return JsonResponse({"status": "error", "message": _("L'adresse email est obligatoire.")}, status=400)

        if NewsletterUser.objects.filter(email=email).exists():
            return JsonResponse({
                "status": "info", 
                "message": _("Vous faites déjà partie de notre cercle privé ! ✨")
            })

        NewsletterUser.objects.create(email=email)
        
        return JsonResponse({
            "status": "success",
            "message": _("Bienvenue ! Votre réduction de -10% vient de vous être réservée. À très vite ! 🤎")
        })

    return JsonResponse({"status": "error", "message": _("Méthode non autorisée.")}, status=405)
