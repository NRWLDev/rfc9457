from __future__ import annotations

from typing import Any


def problem_response(description: str, examples: list[dict], component: str = "Problem") -> dict:
    """Generate an openapi response definition for a problem.

    `examples` should be in the form of marshalled problems.
    """
    examples_ = {
        ex["title"]: {
            "value": ex,
        }
        for ex in examples
    }
    ret_val = {
        "description": description,
        "content": {
            "application/problem+json": {
                "schema": {
                    "$ref": f"#/components/schemas/{component}",
                },
            },
        },
    }
    key = "examples" if len(examples) > 1 else "example"
    ret_val["content"]["application/problem+json"][key] = (
        examples_ if len(examples) > 1 else examples_[examples[0]["title"]]["value"]
    )

    return ret_val


def problem_component(
    title: str,
    required: list[str] | None = None,
    **kwargs: dict[str, Any],
) -> dict:
    """Generate an openapi component definition for a problem."""
    required = required or []
    extras = kwargs or {
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
    }

    return {
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
            **extras,
        },
        "type": "object",
        "required": [
            "type",
            "title",
            "status",
            *required,
        ],
        "title": title,
    }
