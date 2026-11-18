from biblio.repositories.base import connexion


def lister(categorie=None, disponible=None):
    sql = "SELECT * FROM livres WHERE 1=1"
    params = []
    if categorie:
        sql += " AND categorie = ?"
        params.append(categorie)
    if disponible is not None:
        sql += " AND disponible = ?"
        params.append(1 if disponible else 0)
    with connexion() as c:
        return [dict(r) for r in c.execute(sql, params).fetchall()]


def par_id(livre_id):
    with connexion() as c:
        r = c.execute("SELECT * FROM livres WHERE id = ?", (livre_id,)).fetchone()
        return dict(r) if r else None


def ajouter(titre, auteur, categorie):
    with connexion() as c:
        cur = c.execute(
            "INSERT INTO livres (titre, auteur, categorie) VALUES (?, ?, ?)",
            (titre, auteur, categorie),
        )
        return cur.lastrowid


def marquer_disponible(livre_id, disponible):
    with connexion() as c:
        c.execute("UPDATE livres SET disponible = ? WHERE id = ?",
                  (1 if disponible else 0, livre_id))