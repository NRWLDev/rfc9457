import typing

import pytest

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
    e = exc("details")

    assert e.marshal() == {
        "type": type_,
        "title": e.title,
        "details": "details",
        "status": e.status,
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
    e = exc("details")

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
    e = exc("details")

    assert repr(e) == f"{exc.__name__}<title={e.title}; details=details>"


def test_marshal_with_extras():
    e = NotFoundError(key1="value1", key2=["value2", "value3"])

    assert e.marshal() == {
        "type": "not-found",
        "title": "a 404 message",
        "status": 404,
        "key1": "value1",
        "key2": ["value2", "value3"],
    }


def test_marshal_strip_debug():
    e = NotFoundError(details="details", key1="value1", key2=["value2", "value3"])

    assert e.marshal(strip_debug=True) == {
        "type": "not-found",
        "title": "a 404 message",
        "status": 404,
    }


class HeaderError(error.BadRequestProblem):
    headers: typing.ClassVar = {"header1": "value1"}


def test_pass_in_headers():
    e = NotFoundError(details="details", headers={"header1": "value1", "header2": "value2"})

    assert e.headers == {"header1": "value1", "header2": "value2"}


def test_builtin_headers():
    e = HeaderError(details="details")

    assert e.headers == {"header1": "value1"}


def test_augment_headers():
    e = HeaderError(details="details", headers={"header2": "value2"})

    assert e.headers == {"header1": "value1", "header2": "value2"}


def test_replace_headers():
    e = HeaderError(details="details", headers={"header1": "value2"})

    assert e.headers == {"header1": "value2"}
