import pytest
from fastapi.testclient import TestClient

from biblio.repositories import base


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Base temporaire : les tests ne touchent jamais bibliotech.db
    monkeypatch.setattr(base, "DB", str(tmp_path / "test.db"))
    base.initialiser_base()
    from main import app
    return TestClient(app)