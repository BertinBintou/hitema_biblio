from biblio.repositories.base import connexion


def lister():
    with connexion() as c:
        return [dict(r) for r in c.execute("SELECT * FROM utilisateurs").fetchall()]


def par_id(utilisateur_id):
    with connexion() as c:
        r = c.execute("SELECT * FROM utilisateurs WHERE id = ?", (utilisateur_id,)).fetchone()
        return dict(r) if r else None