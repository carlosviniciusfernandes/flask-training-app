from typing import Optional

from models import User
from pydantic import ValidationError
from quart import Blueprint, Response, jsonify, request

users_bp = Blueprint("users", __name__)


class UpdateUserPayload(User):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@users_bp.post("/users/add")
async def add_user() -> tuple[Response, int]:
    payload = await request.get_json()
    try:
        review = User(**payload)
        await review.insert()
        return jsonify(review.model_dump()), 201
    except ValidationError as exc:
        return jsonify({"message": "ValidationError", "extra": exc.json()}), 400


@users_bp.get("/users/<user_id>")
async def get_user(user_id: str) -> tuple[Response, int]:
    user = await User.get(user_id)
    if not user:
        return jsonify({"message": "Not Found"}), 404

    return jsonify(user.model_dump()), 200


@users_bp.patch("/users/<user_id>")
async def update_user(user_id: str) -> tuple[Response, int]:
    body = await request.get_json()
    payload = UpdateUserPayload(**body)

    user = await User.get(user_id)
    if not user:
        return jsonify({"message": "Not Found"}), 404

    for key, value in payload.model_dump(exclude_none=True):
        setattr(user, key, value)
    await user.save()
    return jsonify(user.model_dump()), 200


@users_bp.delete("/users/<user_id>")
async def delete_user(user_id: str) -> tuple[Response, int]:
    user = await User.get(user_id)
    if not user:
        return jsonify({"message": "Not Found"}), 404

    await user.delete()
    return jsonify(None), 204
