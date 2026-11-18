from typing import Optional
from fastapi import APIRouter, HTTPException
from biblio.repositories import livre_repository
from biblio.schemas.livre import LivreCreation

router = APIRouter(prefix="/livres", tags=["Livres"])


@router.get("")
def lister_livres(categorie: Optional[str] = None, disponible: Optional[bool] = None):
    return livre_repository.lister(categorie, disponible)


@router.get("/{livre_id}")
def lire_livre(livre_id: int):
    livre = livre_repository.par_id(livre_id)
    if livre is None:
        raise HTTPException(404, "Livre inconnu")
    return livre


@router.post("", status_code=201)
def ajouter_livre(livre: LivreCreation):
    livre_id = livre_repository.ajouter(livre.titre, livre.auteur, livre.categorie)
    return livre_repository.par_id(livre_id)