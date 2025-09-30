# Python QUIC example

This project demonstrates a basic QUIC server and client implementation in Python using [aioquic](https://aioquic.readthedocs.io/en/latest/) and [Quart](https://quart.palletsprojects.com/en/latest/).

## Prerequisites

- Python 3.8+
- [poetry](https://python-poetry.org/)
- `openssl` (for generating self-signed certificates)
- `make` (for running examples)

To install all dependencies:

```bash
poetry install
```

To get into the virtual environment:

```bash
eval $(poetry env activate)
```

## Examples

### `aioquic` hello world server

You can found a simple aioquic server in [`examples/aioquic/server.py`](./examples/aioquic/server.py). To run it, you can use make, as below.

```bash
make aioquic
```

### `fastapi` application example

> [!NOTE] The HTTP/3 isn't a FastAPI feature, but a [hypercorn](https://pgjones.gitlab.io/hypercorn/) feature.

You can found a simple FastAPI application in [`examples/fastapi/server.py`](./examples/fastapi/server.py). To run it using [hypercorn](https://hypercorn.readthedocs.io/en/latest/), you can use make, as below.

```bash
make fastapi
```

### `curl` for testing the server

You can use `curl` to test the server. HTTP/3 isn't officially supported by stable curl distributions, but we can enable it [compiling curl with HTTP/3 flags](https://curl.se/docs/http3.html). 

To improve the example, I got a ready to use docker image with this setup. At the [`Makefile`](./Makefile) you can find two targets simplifying the process.

To test the server, run:

```bash
make test
```

Or, to see more details:

```bash
make test-verbose
```
