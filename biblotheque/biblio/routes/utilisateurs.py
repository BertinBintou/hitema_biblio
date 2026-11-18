from fastapi import APIRouter, HTTPException
from biblio.repositories import utilisateur_repository

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])


@router.get("")
def lister_utilisateurs():
    return utilisateur_repository.lister()


@router.get("/{utilisateur_id}")
def lire_utilisateur(utilisateur_id: int):
    u = utilisateur_repository.par_id(utilisateur_id)
    if u is None:
        raise HTTPException(404, "Utilisateur inconnu")
    return u