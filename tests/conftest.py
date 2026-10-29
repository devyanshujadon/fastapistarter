import pytest

from app.store import store


@pytest.fixture(autouse=True)
def _fresh_store() -> None:
    store.reset()
