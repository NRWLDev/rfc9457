# Changelog

## v0.0.8 - 2024-05-24

### Bug fixes

- Add in py.typed file so mypy/pyright acknowledge type hints. [[#4](https://github.com/NRWLDev/rfc9457/issues/4)] [[8ce87c1](https://github.com/NRWLDev/rfc9457/commit/8ce87c14f37d28e830b8a9e4c3c5092148fe2a4a)]

## v0.0.7 - 2024-05-23

### Features and Improvements

- Support headers as a first class attribute. [[#1](https://github.com/NRWLDev/rfc9457/issues/1)] [[a6e1bc2](https://github.com/NRWLDev/rfc9457/commit/a6e1bc245c884ff5ab0d40b821bab94b107cc9ca)]

## v0.0.6 - 2024-05-22

### Bug fixes

- Revert to old __str__ method, and introduce __repr__ including details [[e7b7c24](https://github.com/NRWLDev/rfc9457/commit/e7b7c247652acd6e46fe87207e610e4f1d518146)]

## v0.0.5 - 2024-05-21

### Bug fixes

- Don't call super, end the chain at Problem base class. [[c2c63c4](https://github.com/NRWLDev/rfc9457/commit/c2c63c45538c41cd7c835ae7129feb6465b669d3)]

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
