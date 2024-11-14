import typing

import pytest
from multidict import CIMultiDict

import rfc9457 as error


class NotFoundError(error.NotFoundProblem):
    title = "a 404 message"


class InvalidAuthError(error.UnauthorisedProblem):
    title = "a 401 message"


class BadRequestError(error.BadRequestProblem):
    title = "a 400 message"


class ServerExceptionError(error.ServerProblem):
    title = "a 500 message"


@pytest.mark.parametrize(
    ("exc", "type_"),
    [
        (NotFoundError, "not-found"),
        (InvalidAuthError, "invalid-auth"),
        (BadRequestError, "bad-request"),
        (ServerExceptionError, "server-exception"),
    ],
)
def test_marshal(exc, type_):
    e = exc("detail")

    assert e.marshal() == {
        "type": type_,
        "title": e.title,
        "detail": "detail",
        "status": e.status,
    }


def test_marshal_strict_requires_uri():
    e = NotFoundError("detail")

    with pytest.raises(ValueError, match="Strict mode requires a uri template."):
        e.marshal(strict=True)


def test_marshal_strict_defaults_type_to_aboutblank():
    e = NotFoundError("detail")

    assert e.marshal(uri="https://my-docs/errors/{status}/{type}", strict=True) == {
        "type": "about:blank",
        "title": e.title,
        "detail": "detail",
        "status": e.status,
    }


def test_marshal_with_uri():
    e = NotFoundError("detail")

    assert e.marshal(uri="https://my-docs/errors/{status}/{type}") == {
        "type": "https://my-docs/errors/404/not-found",
        "title": "a 404 message",
        "detail": "detail",
        "status": 404,
    }


@pytest.mark.parametrize(
    "exc",
    [
        NotFoundError,
        InvalidAuthError,
        BadRequestError,
        ServerExceptionError,
    ],
)
def test_str(exc):
    e = exc("detail")

    assert str(e) == e.title


@pytest.mark.parametrize(
    "exc",
    [
        NotFoundError,
        InvalidAuthError,
        BadRequestError,
        ServerExceptionError,
    ],
)
def test_repr(exc):
    e = exc("detail")

    assert repr(e) == f"{exc.__name__}<title={e.title}; detail=detail>"


@pytest.mark.parametrize(
    "extra",
    [
        " ",
        "type",
    ],
)
def test_init_with_bad_extras(extra):
    with pytest.raises(ValueError, match=f"Illegal extra keys: {{'{extra}'}}"):
        NotFoundError(**{extra: "value"})


def test_marshal_with_extras():
    e = NotFoundError(key1="value1", key2=["value2", "value3"])

    assert e.marshal() == {
        "type": "not-found",
        "title": "a 404 message",
        "status": 404,
        "key1": "value1",
        "key2": ["value2", "value3"],
    }


class HeaderError(error.BadRequestProblem):
    headers: typing.ClassVar = {"header1": "value1"}


def test_pass_in_headers():
    e = NotFoundError(detail="detail", headers={"header1": "value1", "header2": "value2"})

    assert e.headers == {"header1": "value1", "header2": "value2"}


def test_builtin_headers():
    e = HeaderError(detail="detail")

    assert e.headers == {"header1": "value1"}


def test_augment_headers():
    e = HeaderError(detail="detail", headers={"header2": "value2"})

    assert e.headers == {"header1": "value1", "header2": "value2"}


def test_replace_headers():
    e = HeaderError(detail="detail", headers={"header1": "value2"})

    assert e.headers == {"header1": "value2"}


def test_redirect_location():
    class CustomRedirect(error.RedirectProblem):
        title = "Moved"

    e = CustomRedirect("new-location", "detail")

    assert e.headers == CIMultiDict(Location="new-location")


def test_redirect_location_headers_override():
    class CustomRedirect(error.RedirectProblem):
        title = "Moved"

    e = CustomRedirect("new-location", "detail", headers={"location": "my-location"})

    assert e.headers == CIMultiDict(location="my-location")
