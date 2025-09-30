QUIC_PORT=4433
QUIC_HOST=127.0.0.1

CERT_FILE=cert/cert.pem
KEY_FILE=cert/key.pem


cert:
	@mkdir -p cert
	openssl req -x509 -newkey rsa:4096 -keyout $(KEY_FILE) -out $(CERT_FILE) -days 365 -nodes -subj "/CN=$(QUIC_HOST)"

aioquic: cert
	python examples/aioquic/server.py

fastapi: cert
	hypercorn --quic-bind $(QUIC_HOST):$(QUIC_PORT) --certfile $(CERT_FILE) --keyfile $(KEY_FILE) examples.fastapi.server:app

test:
	docker run --network=host --rm ymuski/curl-http3 curl --http3 --insecure --silent https://$(QUIC_HOST):$(QUIC_PORT)/hello

test-verbose:
	docker run --network=host --rm ymuski/curl-http3 curl --http3 --insecure --silent -vvv https://$(QUIC_HOST):$(QUIC_PORT)/hello
	