# RFC9457 implementation for Python
[![image](https://img.shields.io/pypi/v/rfc9457.svg)](https://pypi.org/project/rfc9457/)
[![image](https://img.shields.io/pypi/l/rfc9457.svg)](https://pypi.org/project/rfc9457/)
[![image](https://img.shields.io/pypi/pyversions/rfc9457.svg)](https://pypi.org/project/rfc9457/)
![style](https://github.com/NRWLDev/rfc9457/actions/workflows/style.yml/badge.svg)
![tests](https://github.com/NRWLDev/rfc9457/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/NRWLDev/rfc9457/branch/main/graph/badge.svg)](https://codecov.io/gh/NRWLDev/rfc9457)

`rfc9457` is a set of exceptions to support easy error management and responses
in web based apis.

Each exception easily marshals to JSON based on the
[RFC9457](https://www.rfc-editor.org/rfc/rfc9457.html) spec for use in api
errors.

This library is currently used to support problem details in both Starlette and FastAPI.

[starlette-problem](https://pypi.org/project/starlette-problem)
[fastapi-problem](https://pypi.org/project/fastapi-problem)

## Custom Errors

Subclassing the convenience classes provides a simple way to consistently raise
the same error with details/extras changing based on the raised context.

```python
from rfc9457.error import NotFoundProblem


class UserNotFoundError(NotFoundProblem):
    title = "User not found."


UserNotFoundError(
    details="details",
    custom_key="value",
).marshal()
```

```json
{
    "type": "user-not-found",
    "title": "User not found",
    "status": 404,
    "details": "details",
    "custom_key": "value",
}
```

## Removing debug information in production

In production environments, it may be desirable to exclude per instance
information to prevent data leakage. In that scenario use `strip_debug` when
marshaling the error.

```python
UserNotFoundError(
    details="details",
    custom_key="value",
).marshal(strip_debug=True)
```

```json
{
    "type": "user-not-found",
    "title": "User not found",
    "status": 404,
}
```
