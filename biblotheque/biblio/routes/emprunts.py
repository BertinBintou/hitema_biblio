from typing import Optional
from fastapi import APIRouter, HTTPException
from biblio.repositories import emprunt_repository
from biblio.schemas.emprunt import EmpruntCreation
from biblio.services import emprunt_service
from biblio.services.exceptions import (
    LivreInconnu, UtilisateurInconnu, LivreDejaEmprunte, QuotaAtteint, EmpruntIntrouvable,
)

router = APIRouter(prefix="/emprunts", tags=["Emprunts"])


@router.get("")
def lister_emprunts(utilisateur_id: Optional[int] = None, historique: bool = False):
    return emprunt_repository.lister(utilisateur_id, historique)


@router.post("", status_code=201)
def emprunter(demande: EmpruntCreation):
    try:
        return emprunt_service.emprunter(demande.livre_id, demande.utilisateur_id)
    except (LivreInconnu, UtilisateurInconnu):
        raise HTTPException(404, "Livre ou utilisateur inconnu")
    except LivreDejaEmprunte:
        raise HTTPException(409, "Livre déjà emprunté")
    except QuotaAtteint:
        raise HTTPException(409, "Quota de 3 emprunts atteint")


@router.post("/retour/{livre_id}")
def rendre(livre_id: int):
    try:
        return emprunt_service.rendre(livre_id)
    except LivreInconnu:
        raise HTTPException(404, "Livre inconnu")
    except EmpruntIntrouvable:
        raise HTTPException(409, "Ce livre n'est pas emprunté")