from sqlmodel import Session, SQLModel, create_engine

sqlite_url = "sqlite:///bank.db"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
