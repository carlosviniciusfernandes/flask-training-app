from typing import Optional

from models import Review, User
from pydantic import BaseModel
from quart import Blueprint, Response, jsonify, request

reviews_bp = Blueprint("reviews", __name__)


class AddReviewPayload(Review): ...


class UpdateReviewPayload(BaseModel):
    description: Optional[str] = None


@reviews_bp.post("/users/<user_id>/reviews/add")
async def add_review(user_id: str) -> tuple[Response, int]:
    body = await request.get_json()
    payload = AddReviewPayload(**body)

    user = await User.get(user_id)
    if not user:
        return jsonify({"message": "ValidationError", "extra": {"user_id": f"No user was found"}}), 400

    user.reviews.append(payload.review)
    await user.save()
    return jsonify(user.model_dump()), 201


@reviews_bp.get("/users/<user_id>/reviews/<review_id>")
async def get_review(user_id: str, review_id: str) -> tuple[Response, int]:
    user = await User.get(user_id)
    if not user:
        return jsonify({"message": "ValidationError", "extra": {"user_id": f"No user was found"}}), 400

    review = user.reviews.get(review_id)
    if not review:
        return jsonify({"message": "Not Found"}), 404

    return jsonify(review.model_dump()), 201


@reviews_bp.patch("/users/<user_id>/reviews/<review_id>")
async def update_review(user_id: str, review_id: str) -> tuple[Response, int]:
    body = await request.get_json()
    payload = UpdateReviewPayload(**body)

    user = await User.get(user_id)
    if not user:
        return jsonify({"message": "ValidationError", "extra": {"user_id": f"No user was found"}}), 400

    review = user.reviews.get(review_id)
    if not review:
        return jsonify({"message": "Not Found"}), 404

    for key, value in payload.model_dump(exclude_none=True):
        setattr(review, key, value)
    await user.save()
    return jsonify(user.model_dump()), 200


@reviews_bp.delete("/users/<user_id>/reviews/<review_id>")
async def delete_review(user_id: str, review_id: str) -> tuple[Response, int]:
    user = await User.get(user_id)
    if not user:
        return jsonify({"message": "ValidationError", "extra": {"user_id": f"No user was found"}}), 400

    review = user.reviews.get(review_id)
    if not review:
        return jsonify({"message": "Not Found"}), 404

    await user.save()
    return jsonify(None), 204
