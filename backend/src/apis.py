from flask import Response
from flask import current_app as app
from flask import jsonify, request
from models import Review, User
from pydantic import ValidationError


@app.post("/reviews/add")
async def add_review() -> tuple[Response, int]:
    payload = request.json
    review = Review(**payload)
    return jsonify(review.model_dump()), 201


@app.post("/users/add")
async def add_user() -> tuple[Response, int]:
    payload = request.json
    try:
        review = User(**payload)
        await review.insert()
        return jsonify(review.model_dump()), 201
    except ValidationError as exc:
        return jsonify({"message": "ValidationError", "extra": exc.json()}), 400
