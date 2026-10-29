from app.schemas import Item, ItemCreate, ItemUpdate, User, UserCreate


class ConflictError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class Store:
    """In-memory stand-in for a database. Swap this for a real store later."""

    def __init__(self) -> None:
        self.items: dict[int, Item] = {}
        self.users: dict[int, User] = {}
        self._item_seq = 0
        self._user_seq = 0

    def reset(self) -> None:
        self.items.clear()
        self.users.clear()
        self._item_seq = 0
        self._user_seq = 0
        self.seed()

    def seed(self) -> None:
        self.create_item(
            ItemCreate(
                name="Notebook",
                description="Hardcover A5",
                price=12.5,
                tags=["stationery"],
            )
        )
        self.create_item(
            ItemCreate(
                name="Coffee mug",
                description="12oz ceramic",
                price=18.0,
                tags=["kitchen"],
            )
        )
        self.create_user(
            UserCreate(name="Ada Lovelace", email="ada@example.com", role="admin")
        )
        self.create_user(UserCreate(name="Alan Turing", email="alan@example.com"))

    def list_items(self, *, tag: str | None = None, q: str | None = None) -> list[Item]:
        found = list(self.items.values())
        if tag is not None:
            found = [item for item in found if tag in item.tags]
        if q:
            needle = q.casefold()
            found = [item for item in found if needle in item.name.casefold()]
        return found

    def get_item(self, item_id: int) -> Item | None:
        return self.items.get(item_id)

    def create_item(self, payload: ItemCreate) -> Item:
        self._item_seq += 1
        item = Item(id=self._item_seq, **payload.model_dump())
        self.items[item.id] = item
        return item

    def update_item(self, item_id: int, payload: ItemUpdate) -> Item | None:
        current = self.items.get(item_id)
        if current is None:
            return None
        updates = payload.model_dump(exclude_unset=True)
        updated = current.model_copy(update=updates)
        self.items[item_id] = updated
        return updated

    def delete_item(self, item_id: int) -> bool:
        return self.items.pop(item_id, None) is not None

    def list_users(self, *, role: str | None = None) -> list[User]:
        found = list(self.users.values())
        if role is not None:
            found = [user for user in found if user.role == role]
        return found

    def get_user(self, user_id: int) -> User | None:
        return self.users.get(user_id)

    def create_user(self, payload: UserCreate) -> User:
        email = str(payload.email).lower()
        if any(user.email.lower() == email for user in self.users.values()):
            raise ConflictError(f"A user with email {email} already exists")
        self._user_seq += 1
        user = User(id=self._user_seq, name=payload.name, email=email, role=payload.role)
        self.users[user.id] = user
        return user


store = Store()
store.seed()
