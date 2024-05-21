# Changelog

## v0.0.4 - 2024-05-17

### Bug fixes

- Store status as status_code attribute to work around sentry implementation for sentry_sdk.

## v0.0.3 - 2024-05-16

### Bug fixes

- Provide overridable cls tuple `__mandatory__` to determine which keys get kept when stripping debug. [[a339dbc](https://github.com/NRWLDev/rfc9457/commit/a339dbc882e2ebc467728444933f9e33999684a3)]

## v0.0.2 - 2024-05-16

### Bug fixes

- Extract error to type helper function from class. [[f4b1605](https://github.com/NRWLDev/rfc9457/commit/f4b160543c9e13ed2bcfdd5411dc3492d3b4b63e)]

## v0.0.1 - 2024-05-16

### Features and Improvements

- Implement Problem baseclass from fastapi-problem library. [[23bdc33](https://github.com/NRWLDev/rfc9457/commit/23bdc33e70d542ae134b76cc2b07e0b389df600b)]
