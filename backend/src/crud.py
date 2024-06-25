from typing import TypeVar

from beanie import Document
from werkzeug.exceptions import NotFound

D = TypeVar("D", bound=Document)


async def get_object_or_404(doc: type[D], id: str) -> type[D]:
    obj = await doc.get(id)
    if not obj:
        raise NotFound("Not Found")
    return obj


async def update_object(doc: type[D], values: dict) -> type[D]:
    for key, value in values.items():
        setattr(doc, key, value)
    await doc.save()
    return doc
