from pydantic import BaseModel


class EmpruntCreation(BaseModel):
    livre_id: int
    utilisateur_id: int