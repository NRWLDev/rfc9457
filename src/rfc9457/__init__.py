"""Implement RFC9547 compatible exceptions.

https://www.rfc-editor.org/rfc/rfc9457.html
"""

from __future__ import annotations

import re
import typing as t

CONVERT_RE = re.compile(r"(?<!^)(?=[A-Z])")


def error_class_to_type(exc: Exception) -> str:
    """Convert an exception class name to a `problem-type` string."""
    type_ = "".join(exc.__class__.__name__.rsplit("Error", 1))
    return CONVERT_RE.sub("-", type_).lower()


class Problem(Exception):  # noqa: N818
    """
    A base exception designed to support all API error handling.
    All exceptions should inherit from this or a subclass of it (depending on the usage),
    this will allow all apps and libraries to maintain a common exception chain.
    """

    __mandatory__ = ("type", "title", "status")

    def __init__(
        self: t.Self,
        title: str,
        type_: str | None = None,
        details: str | None = None,
        status: int = 500,
        **kwargs,
    ) -> None:
        super().__init__(title)
        self._type = type_
        self.title = title
        self.details = details
        self.status = status
        self.extras = kwargs

    @property
    def type(self: t.Self) -> str:
        type_ = error_class_to_type(self)
        return self._type if self._type else type_

    def marshal(self: t.Self, *, strip_debug: bool = False) -> dict[str, t.Any]:
        """Generate a JSON compatible representation.

        Args:
        ----
            strip_debug: If true, remove anything that is not title/type.
        """
        ret = {
            "type": self.type,
            "title": self.title,
            "status": self.status,
        }

        if self.details:
            ret["details"] = self.details

        for k, v in self.extras.items():
            ret[k] = v

        if strip_debug:
            ret = {k: v for k, v in ret.items() if k in self.__mandatory__}

        return ret


class StatusProblem(Problem):
    code = None
    type_ = None
    title = "Base http exception."
    status = 500

    def __init__(self: t.Self, details: str | None = None, **kwargs) -> None:
        super().__init__(self.title, type_=self.type_ or self.code, details=details, status=self.status, **kwargs)


class ServerProblem(StatusProblem): ...


class BadRequestProblem(StatusProblem):
    status = 400


class UnauthorisedProblem(StatusProblem):
    status = 401


class ForbiddenProblem(StatusProblem):
    status = 403


class NotFoundProblem(StatusProblem):
    status = 404


class ConflictProblem(StatusProblem):
    status = 409


class UnprocessableProblem(StatusProblem):
    status = 422
