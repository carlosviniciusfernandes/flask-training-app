from pydantic import ValidationError as PydanticValidationError
from quart import Quart, jsonify, request
from werkzeug.exceptions import HTTPException


def register_exception_handlers(app: Quart):

    @app.errorhandler(HTTPException)
    async def handle_http_exception(error: HTTPException):
        response = {
            "detail": str(error.description),
        }
        return jsonify(response), error.code

    @app.errorhandler(PydanticValidationError)
    async def handle_pydantic_validation_error(error: PydanticValidationError):
        print(error.errors())
        response = {
            "detail": "Validation Error",
            "extra": {"errors": [e for e in error.errors(include_context=False, include_url=False, include_input=False)]},
        }
        return jsonify(response), 400
