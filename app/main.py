from fastapi import FastAPI

app = FastAPI(
    title="Futurisys ML API",
    description="Projet 5 OCR - API de classification automatique basée sur le modèle du Projet 4.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Acceuil de l'API pour Futurisys !",
        "status": "online",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
