from biblio.repositories import livre_repository, utilisateur_repository, emprunt_repository
from biblio.services.exceptions import (
    LivreInconnu, UtilisateurInconnu, LivreDejaEmprunte, QuotaAtteint, EmpruntIntrouvable,
)

QUOTA = 3


def emprunter(livre_id, utilisateur_id):
    livre = livre_repository.par_id(livre_id)
    if livre is None:
        raise LivreInconnu(livre_id)
    if utilisateur_repository.par_id(utilisateur_id) is None:
        raise UtilisateurInconnu(utilisateur_id)

    # RÈGLE 1 : un emprunt à la fois
    if not livre["disponible"]:
        raise LivreDejaEmprunte(livre_id)

    # RÈGLE 2 : trois emprunts au plus
    if emprunt_repository.compter_en_cours(utilisateur_id) >= QUOTA:
        raise QuotaAtteint(utilisateur_id)

    emprunt_id = emprunt_repository.ajouter(livre_id, utilisateur_id)
    livre_repository.marquer_disponible(livre_id, False)
    return {"id": emprunt_id, "livre_id": livre_id, "utilisateur_id": utilisateur_id}


def rendre(livre_id):
    if livre_repository.par_id(livre_id) is None:
        raise LivreInconnu(livre_id)
    emprunt = emprunt_repository.emprunt_en_cours_du_livre(livre_id)
    if emprunt is None:
        raise EmpruntIntrouvable(livre_id)

    # RÈGLE 3 : le retour libère
    emprunt_repository.cloturer(emprunt["id"])
    livre_repository.marquer_disponible(livre_id, True)
    return {"livre_id": livre_id, "message": "Livre rendu"}