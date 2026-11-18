from pydantic import BaseModel


class LivreCreation(BaseModel):
    titre: str
    auteur: str
    categorie: str