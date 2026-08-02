from sqlmodel import Field, SQLModel, create_engine, Session

sqlite_url = f"sqlite:///tasks.db"

class Tasks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def populate_db():
    TASKS = [
        {"id": 1, "title": "Buy groceries", "done": False},
        {"id": 2, "title": "Walk the dog", "done": True},
        {"id": 3, "title": "Read a book", "done": False},
    ]
    
    with Session(engine) as session:
        for task in TASKS:
            session.add(Tasks(title=task["title"], done=task["done"]))
        session.commit()