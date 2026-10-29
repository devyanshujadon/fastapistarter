from fastapi import APIRouter, HTTPException, Query, status

from app.schemas import Item, ItemCreate, ItemUpdate, Page
from app.store import store

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=Page[Item])
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    tag: str | None = None,
    q: str | None = Query(None, description="Case-insensitive match on the item name"),
) -> Page[Item]:
    found = store.list_items(tag=tag, q=q)
    return Page(results=found[skip : skip + limit], total=len(found), skip=skip, limit=limit)


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> Item:
    return store.create_item(payload)


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = store.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.patch("/{item_id}", response_model=Item)
def update_item(item_id: int, payload: ItemUpdate) -> Item:
    item = store.update_item(item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    if not store.delete_item(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
