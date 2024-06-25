from typing import Optional

from crud import get_object_or_404, update_object
from models import Review, User
from pydantic import BaseModel
from quart import Blueprint, Response, jsonify, request
from werkzeug.exceptions import NotFound

reviews_bp = Blueprint("reviews", __name__)


class UpdateReviewPayload(BaseModel):
    description: Optional[str] = None


def _get_review_from_user(user: User, review_id: str) -> Review:
    review = user.reviews.get(review_id)
    if not review:
        raise NotFound("Not Found")
    return review


@reviews_bp.post("/users/<user_id>/reviews/add")
async def add_review(user_id: str) -> tuple[Response, int]:
    body = await request.get_json()
    new_review = Review(**body)

    user = await get_object_or_404(User, user_id)
    review_id = int(new_review.created_at.timestamp())
    if not user.reviews:
        user.reviews = {review_id: new_review}
    else:
        user.reviews[review_id] = new_review
    await user.save()

    return jsonify(user.model_dump()), 201


@reviews_bp.get("/users/<user_id>/reviews/<review_id>")
async def get_review(user_id: str, review_id: str) -> tuple[Response, int]:
    user = await get_object_or_404(User, user_id)
    review = _get_review_from_user(user, review_id)
    return jsonify(review.model_dump()), 200


@reviews_bp.patch("/users/<user_id>/reviews/<review_id>")
async def update_review(user_id: str, review_id: str) -> tuple[Response, int]:
    body = await request.get_json()
    payload = UpdateReviewPayload(**body)

    user = await get_object_or_404(User, user_id)
    review = _get_review_from_user(user, review_id)
    user.reviews[int(review.created_at.timestamp())] = {"description": payload.description}
    await user.save()

    return jsonify(user.model_dump()), 200


@reviews_bp.delete("/users/<user_id>/reviews/<review_id>")
async def delete_review(user_id: str, review_id: str) -> tuple[Response, int]:
    user = await get_object_or_404(User, user_id)
    review = _get_review_from_user(user, review_id)

    del user.reviews[review_id]
    await user.save()

    return jsonify(None), 204
