def emprunter(client, livre_id, utilisateur_id):
    return client.post("/emprunts", json={"livre_id": livre_id, "utilisateur_id": utilisateur_id})


def test_emprunter(client):
    r = emprunter(client, 1, 1)
    assert r.status_code == 201
    assert client.get("/livres/1").json()["disponible"] == 0


def test_regle1_livre_deja_emprunte(client):
    emprunter(client, 1, 1)
    assert emprunter(client, 1, 2).status_code == 409


def test_regle2_quota_de_3(client):
    for livre in (1, 2, 3):
        assert emprunter(client, livre, 1).status_code == 201
    assert emprunter(client, 4, 1).status_code == 409


def test_regle3_le_retour_libere(client):
    emprunter(client, 1, 1)
    assert client.post("/emprunts/retour/1").status_code == 200
    assert client.get("/livres/1").json()["disponible"] == 1
    assert emprunter(client, 1, 2).status_code == 201


def test_retour_libere_une_place_du_quota(client):
    for livre in (1, 2, 3):
        emprunter(client, livre, 1)
    client.post("/emprunts/retour/1")
    assert emprunter(client, 4, 1).status_code == 201


def test_emprunter_livre_inconnu(client):
    assert emprunter(client, 999, 1).status_code == 404


def test_emprunter_utilisateur_inconnu(client):
    assert emprunter(client, 1, 999).status_code == 404


def test_rendre_livre_non_emprunte(client):
    assert client.post("/emprunts/retour/1").status_code == 409


def test_liste_emprunts_et_historique(client):
    emprunter(client, 1, 1)
    emprunter(client, 2, 1)
    client.post("/emprunts/retour/1")
    assert len(client.get("/emprunts?utilisateur_id=1").json()) == 1
    assert len(client.get("/emprunts?utilisateur_id=1&historique=true").json()) == 2