from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import (
    create_artwork,
    get_active_artworks,
    get_all_artworks
)

from app.db import SessionLocal
from app.schemas import ArtworkCreate


router = APIRouter(
    prefix="/artworks",
    tags=["Artworks"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_artwork(
    artwork: ArtworkCreate,
    db: Session = Depends(get_db)
):
    return create_artwork(db, artwork)


@router.get("/")
def artworks(
    db: Session = Depends(get_db)
):
    return get_all_artworks(db)


@router.get("/active")
def active_artworks(
    db: Session = Depends(get_db)
):
    return get_active_artworks(db)