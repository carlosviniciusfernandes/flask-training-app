from typing import Optional

from crud import get_object_or_404, update_object
from models import User
from quart import Blueprint, Response, jsonify, request

users_bp = Blueprint("users", __name__)


class UpdateUserPayload(User):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@users_bp.post("/users/add")
async def add_user() -> tuple[Response, int]:
    payload = await request.get_json()

    review = User(**payload)
    await review.insert()

    return jsonify(review.model_dump()), 201


@users_bp.get("/users/<user_id>")
async def get_user(user_id: str) -> tuple[Response, int]:
    user = await get_object_or_404(User, user_id)
    return jsonify(user.model_dump()), 200


@users_bp.patch("/users/<user_id>")
async def update_user(user_id: str) -> tuple[Response, int]:
    body = await request.get_json()
    payload = UpdateUserPayload(**body)

    user = await get_object_or_404(User, user_id)
    await update_object(user, payload.model_dump(exclude_none=True))

    return jsonify(user.model_dump()), 200


@users_bp.delete("/users/<user_id>")
async def delete_user(user_id: str) -> tuple[Response, int]:
    user = await get_object_or_404(User, user_id)

    await user.delete()

    return jsonify(None), 204
