from biblio.repositories.base import connexion


def compter_en_cours(utilisateur_id):
    with connexion() as c:
        return c.execute(
            "SELECT COUNT(*) FROM emprunts WHERE utilisateur_id = ? AND date_retour IS NULL",
            (utilisateur_id,),
        ).fetchone()[0]


def ajouter(livre_id, utilisateur_id):
    with connexion() as c:
        cur = c.execute(
            "INSERT INTO emprunts (livre_id, utilisateur_id) VALUES (?, ?)",
            (livre_id, utilisateur_id),
        )
        return cur.lastrowid


def emprunt_en_cours_du_livre(livre_id):
    with connexion() as c:
        r = c.execute(
            "SELECT * FROM emprunts WHERE livre_id = ? AND date_retour IS NULL",
            (livre_id,),
        ).fetchone()
        return dict(r) if r else None


def cloturer(emprunt_id):
    with connexion() as c:
        c.execute("UPDATE emprunts SET date_retour = datetime('now') WHERE id = ?", (emprunt_id,))


def lister(utilisateur_id=None, historique=False):
    sql = """
        SELECT e.id, e.livre_id, l.titre, e.utilisateur_id, u.nom AS utilisateur,
               e.date_emprunt, e.date_retour
        FROM emprunts e
        JOIN livres l ON l.id = e.livre_id
        JOIN utilisateurs u ON u.id = e.utilisateur_id
        WHERE 1=1
    """
    params = []
    if utilisateur_id:
        sql += " AND e.utilisateur_id = ?"
        params.append(utilisateur_id)
    if not historique:
        sql += " AND e.date_retour IS NULL"
    sql += " ORDER BY e.id"
    with connexion() as c:
        return [dict(r) for r in c.execute(sql, params).fetchall()]