from app.db.database import Base, engine
from app.models import book, review  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
