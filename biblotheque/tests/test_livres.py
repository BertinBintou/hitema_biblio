def test_accueil(client):
    assert client.get("/").status_code == 200


def test_lister_livres(client):
    r = client.get("/livres")
    assert r.status_code == 200
    assert len(r.json()) == 6


def test_filtrer_par_categorie(client):
    r = client.get("/livres?categorie=Roman")
    assert len(r.json()) == 3


def test_lire_un_livre(client):
    assert client.get("/livres/1").json()["titre"] == "Le Petit Prince"


def test_livre_inconnu(client):
    assert client.get("/livres/999").status_code == 404


def test_ajouter_livre(client):
    r = client.post("/livres", json={"titre": "Candide", "auteur": "Voltaire", "categorie": "Conte"})
    assert r.status_code == 201
    assert r.json()["disponible"] == 1


def test_lister_utilisateurs(client):
    assert len(client.get("/utilisateurs").json()) == 4