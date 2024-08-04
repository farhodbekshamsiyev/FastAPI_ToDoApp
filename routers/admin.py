from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, Path
from sqlalchemy.orm import Session
from starlette import status

from db_config import SessionLocal
from models import Todos
from routers.auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if not user or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if not user or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    todo_model = db.query(Todos).filter(todo_id == Todos.id).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.query(Todos).filter(todo_id == Todos.id).delete()
    db.commit()
