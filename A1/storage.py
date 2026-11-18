from sqlmodel import Field, SQLModel, create_engine, Session, select, col
from model import Item as TaskItem

sqlite_url = f"sqlite:///tasks.db"

class Tasks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False


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

def delete_task(id: int):
    with Session(engine) as session:
        task = session.get(Tasks, id)
        
        if not task:
            return False
        
        session.delete(task)
        session.commit()
        
        return True
        
def update_task(id: int, item: TaskItem):
    with Session(engine) as session:
        task = session.get(Tasks, id)
        
        if not task:
            return None
        
        update_data = item.model_dump(exclude_unset=True)
        task.sqlmodel_update(update_data)
        
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return task

def create_task(title: str):
    with Session(engine) as session:
        task = Tasks(title=title)
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return task

def get_tasks(search: str | None = None, done: bool | None = None):
    with Session(engine) as session:
        statement = select(Tasks)
        if search:
            statement = statement.where(col(Tasks.title).ilike(f"%{search}%"))
        
        if done is not None:
            statement = statement.where(Tasks.done == done)
        
        return session.exec(statement).all()
    
def get_task(id: int):
    with Session(engine) as session:    
        return session.get(Tasks, id)