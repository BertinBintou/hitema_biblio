import uvicorn
from fastapi import FastAPI

from biblio.repositories.base import initialiser_base
from biblio.routes import livres, utilisateurs, emprunts

initialiser_base()

app = FastAPI(title="BiblioTech")
app.include_router(livres.router)
app.include_router(utilisateurs.router)
app.include_router(emprunts.router)


@app.get("/")
def accueil():
    return {"message": "BiblioTech : ouvrez /docs pour tester"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)