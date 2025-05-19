from rfc9457 import Problem
from rfc9457.openapi import problem_component, problem_response


def test_problem_response():
    assert problem_response(
        description="Client Error",
        examples=[
            Problem(
                title="User facing error message.",
                type_="client-error-type",
                status=400,
                detail="Additional error context.",
            ).marshal(),
        ],
    ) == {
        "content": {
            "application/problem+json": {
                "schema": {
                    "$ref": "#/components/schemas/Problem",
                },
                "example": {
                    "title": "User facing error message.",
                    "detail": "Additional error context.",
                    "type": "client-error-type",
                    "status": 400,
                },
            },
        },
        "description": "Client Error",
    }


def test_problem_response_multiple_examples():
    assert problem_response(
        description="Client Error",
        examples=[
            Problem(
                title="User facing error message.",
                type_="client-error-type",
                status=400,
                detail="Additional error context.",
            ).marshal(),
            Problem(
                title="Another user facing error message.",
                type_="another-client-error-type",
                status=400,
                detail="Additional error context.",
            ).marshal(),
        ],
    ) == {
        "content": {
            "application/problem+json": {
                "schema": {
                    "$ref": "#/components/schemas/Problem",
                },
                "examples": {
                    "User facing error message.": {
                        "value": {
                            "title": "User facing error message.",
                            "detail": "Additional error context.",
                            "type": "client-error-type",
                            "status": 400,
                        },
                    },
                    "Another user facing error message.": {
                        "value": {
                            "title": "Another user facing error message.",
                            "detail": "Additional error context.",
                            "type": "another-client-error-type",
                            "status": 400,
                        },
                    },
                },
            },
        },
        "description": "Client Error",
    }


def test_problem_component():
    assert problem_component("Problem") == {
        "properties": {
            "title": {
                "type": "string",
                "title": "Problem title",
            },
            "type": {
                "type": "string",
                "title": "Problem type",
            },
            "status": {
                "type": "integer",
                "title": "Status code",
            },
            "detail": {
                "anyOf": [
                    {
                        "type": "string",
                    },
                    {
                        "type": "null",
                    },
                ],
                "title": "Problem detail",
            },
        },
        "type": "object",
        "required": [
            "type",
            "title",
            "status",
        ],
        "title": "Problem",
    }


def test_custom_problem_component():
    assert problem_component(
        "RequestValidationError",
        required=["errors"],
        errors={
            "type": "array",
            "items": {
                "$ref": "#/components/schemas/ValidationError",
            },
        },
    ) == {
        "properties": {
            "title": {
                "type": "string",
                "title": "Problem title",
            },
            "type": {
                "type": "string",
                "title": "Problem type",
            },
            "status": {
                "type": "integer",
                "title": "Status code",
            },
            "errors": {
                "type": "array",
                "items": {
                    "$ref": "#/components/schemas/ValidationError",
                },
            },
        },
        "type": "object",
        "required": [
            "type",
            "title",
            "status",
            "errors",
        ],
        "title": "RequestValidationError",
    }
