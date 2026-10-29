from fastapi import APIRouter, HTTPException, Query, status

from app.schemas import Page, User, UserCreate
from app.store import store

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=Page[User])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    role: str | None = Query(None, pattern="^(admin|member)$"),
) -> Page[User]:
    found = store.list_users(role=role)
    return Page(results=found[skip : skip + limit], total=len(found), skip=skip, limit=limit)


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate) -> User:
    return store.create_user(payload)


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    user = store.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
