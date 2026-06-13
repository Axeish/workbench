from sqlalchemy.orm import Session

from app.models import Artwork


def create_artwork(
    db: Session,
    artwork_data
):
    artwork = Artwork(
        title=artwork_data.title,
        artist_id=artwork_data.artist_id,
        status=artwork_data.status,
        notes=artwork_data.notes
    )

    db.add(artwork)
    db.commit()
    db.refresh(artwork)

    return artwork


def get_all_artworks(db: Session):
    return db.query(Artwork).all()


def get_active_artworks(db: Session):
    return (
        db.query(Artwork)
        .filter(Artwork.status == "ACTIVE")
        .all()
    )