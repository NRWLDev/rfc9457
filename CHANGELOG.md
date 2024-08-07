# Changelog

## v0.1.0 - 2024-07-23

### Bug fixes

- **Breaking:** Correctly match the RFC9457 spec with detail not details. [[#8](https://github.com/NRWLDev/rfc9457/issues/8)] [[59a3325](https://github.com/NRWLDev/rfc9457/commit/59a33254386ec677209945871f0182914c403dd7)]

### Miscellaneous

- Update changelog-gen dependency [[b4a897f](https://github.com/NRWLDev/rfc9457/commit/b4a897fbaaf6da55e181485ea294fdc62adf1b06)]

## v0.0.11 - 2024-06-28

- Update README with details of libraries making use of code.

## v0.0.10 - 2024-05-31

### Features and Improvements

- Add support for type base urls on marshal. [[#6](https://github.com/NRWLDev/rfc9457/issues/6)] [[8b50ee0](https://github.com/NRWLDev/rfc9457/commit/8b50ee02c5b8bde6aee96c5d6e7ccf580fca04d7)]

## v0.0.9 - 2024-05-31

### Features and Improvements

- Add support for Redirect base class with explicit location argument. [[#3](https://github.com/NRWLDev/rfc9457/issues/3)] [[e805089](https://github.com/NRWLDev/rfc9457/commit/e80508967109c216a17b1bb17b91c9d0dce581d2)]

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
