import sqlite3

DB = "bibliotech.db"


def connexion():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def initialiser_base():
    with connexion() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            categorie TEXT NOT NULL,
            disponible INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS emprunts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livre_id INTEGER NOT NULL REFERENCES livres(id),
            utilisateur_id INTEGER NOT NULL REFERENCES utilisateurs(id),
            date_emprunt TEXT NOT NULL DEFAULT (datetime('now')),
            date_retour TEXT
        );
        """)

        if c.execute("SELECT COUNT(*) FROM utilisateurs").fetchone()[0] == 0:
            c.executescript("""
            INSERT INTO utilisateurs (nom, email) VALUES ('Léa Martin',   'lea@mail.fr');
            INSERT INTO utilisateurs (nom, email) VALUES ('Tom Durand',   'tom@mail.fr');
            INSERT INTO utilisateurs (nom, email) VALUES ('Sara Benali',  'sara@mail.fr');
            INSERT INTO utilisateurs (nom, email) VALUES ('Yanis Moreau', 'yanis@mail.fr');
            """)

        if c.execute("SELECT COUNT(*) FROM livres").fetchone()[0] == 0:
            c.executescript("""
            INSERT INTO livres (titre, auteur, categorie) VALUES ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Conte');
            INSERT INTO livres (titre, auteur, categorie) VALUES ('1984',            'George Orwell',            'Science-fiction');
            INSERT INTO livres (titre, auteur, categorie) VALUES ('Dune',            'Frank Herbert',            'Science-fiction');
            INSERT INTO livres (titre, auteur, categorie) VALUES ('L''Étranger',     'Albert Camus',             'Roman');
            INSERT INTO livres (titre, auteur, categorie) VALUES ('Germinal',        'Émile Zola',               'Roman');
            INSERT INTO livres (titre, auteur, categorie) VALUES ('Les Misérables',  'Victor Hugo',              'Roman');
            """)