QUIC_PORT=4433
QUIC_HOST=localhost

CERT_FILE=cert/cert.pem
KEY_FILE=cert/key.pem


cert:
	@mkdir -p cert
	openssl req -x509 -newkey rsa:4096 -keyout $(KEY_FILE) -out $(CERT_FILE) -days 365 -nodes -subj "/CN=$(QUIC_HOST)"

quart: cert
	hypercorn --quic-bind $(QUIC_HOST):$(QUIC_PORT) --certfile $(CERT_FILE) --keyfile $(KEY_FILE) examples.quart.app:app

test:
	docker run --network=host --rm ymuski/curl-http3 curl --http3 --insecure --silent https://$(QUIC_HOST):$(QUIC_PORT)/hello