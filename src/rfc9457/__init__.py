"""Implement RFC9547 compatible exceptions.

https://www.rfc-editor.org/rfc/rfc9457.html
"""

from __future__ import annotations

import re
import typing as t
from warnings import warn

from multidict import CIMultiDict

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

    def __init__(  # noqa: PLR0913
        self: t.Self,
        title: str,
        type_: str | None = None,
        detail: str | None = None,
        status: int = 500,
        headers: CIMultiDict[str, str] | None = None,
        **kwargs,
    ) -> None:
        self._type = type_
        self.title = title
        self.detail = detail
        self.status = status
        self.status_code = status  # work around for sentry integrations that expect status_code attr
        self.headers = headers
        self.extras = kwargs

        bad_extras = {k for k in self.extras if k in {"type"} or not k.strip()}
        if len(bad_extras) > 0:
            msg = f"Illegal extra keys: {bad_extras}"
            raise ValueError(msg)

    def __str__(self: t.Self) -> str:
        return self.title

    def __repr__(self: t.Self) -> str:
        return f"{self.__class__.__name__}<title={self.title}; detail={self.detail}>"

    @property
    def type(self: t.Self) -> str:
        return self._type if self._type else error_class_to_type(self)

    def marshal(
        self: t.Self,
        type_base_url: str | None = None,
        *,
        uri: str = "",
        strip_debug: bool = False,
        strict: bool = False,
    ) -> dict[str, t.Any]:
        """Generate a JSON compatible representation.

        Provide a uri template to expand internal parameters into a full type uri
        Example: "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{status}"

        Args:
        ----
            type_base_url: If provided prepend to the type to generate a full url. (DEPRECATED; use uri instead)
            uri: URI / URI template to use as the type; will substitute '{status}', '{title}', '{type}', and **extras.
            strip_debug: If true, remove anything that is not title/type.
            strict: If true, enforce type as a uri, and treat unset types as 'about:blank'.
        """
        type_ = self.type
        if type_base_url:
            type_ = f"{type_base_url}{self.type}"
            warn(
                "Using deprecated parameter 'type_base_url', switch to 'uri'",
                FutureWarning,
                stacklevel=2,
            )

        if strict and not uri:
            msg = "Strict mode requires a uri template."
            raise ValueError(msg)

        if strict and not self._type:
            type_ = "about:blank"

        elif uri:
            type_ = uri.format(status=self.status, type=self.type, title=self.title, **self.extras)

        optional = self.extras.copy()
        if self.detail:
            optional["detail"] = self.detail

        return {
            "type": type_,
            "title": self.title,
            "status": self.status,
            # if strip_debug, restrict optional extras to __mandatory__
            **{k: v for k, v in optional.items() if k in self.__mandatory__ or not strip_debug},
        }


class StatusProblem(Problem):
    code: str | None = None
    type_: str | None = None
    title: str = "Base http exception."
    status: int = 500
    headers: CIMultiDict[str, str] | None = None

    def __init__(
        self: t.Self,
        detail: str | None = None,
        headers: CIMultiDict[str, str] | None = None,
        **kwargs,
    ) -> None:
        headers_ = (self.headers or {}).copy()
        if headers:
            headers_.update(headers)

        super().__init__(
            self.title,
            type_=self.type_ or self.code,
            detail=detail,
            status=self.status,
            headers=headers_ or None,
            **kwargs,
        )


class ServerProblem(StatusProblem): ...


class RedirectProblem(StatusProblem):
    status = 301

    def __init__(
        self: t.Self,
        location: str,
        detail: str | None = None,
        headers: CIMultiDict[str, str] | None = None,
        **kwargs,
    ) -> None:
        headers_ = CIMultiDict(Location=location)
        headers_.update(headers or {})
        super().__init__(detail=detail, headers=headers_, **kwargs)


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
