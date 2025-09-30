import asyncio

from aioquic.asyncio.server import serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol, QuicStreamHandler
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.h3.events import HeadersReceived
from aioquic.quic.events import QuicEvent

from examples.settings import CERTIFY_PATH, KEY_PATH


class HelloQuicProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._http = H3Connection(self._quic)

    def quic_event_received(self, event: QuicEvent):
        for http_event in self._http.handle_event(event):
            if isinstance(http_event, HeadersReceived):
                print(http_event.headers)
                self._http.send_headers(
                    stream_id=http_event.stream_id,
                    headers=[
                        (b':status', b'200'),
                        (b'content-type', b'text/plain')
                    ],
                )
                self._http.send_data(
                    stream_id=http_event.stream_id,
                    data=b"hello world\n",
                    end_stream=True
                )
                self.transmit()
                

async def main():
    config = QuicConfiguration(is_client=False, alpn_protocols=H3_ALPN)
    config.load_cert_chain(certfile=CERTIFY_PATH, keyfile=KEY_PATH)
    
    try:
        await serve(
            host="0.0.0.0",
            port=4433,
            configuration=config,
            create_protocol=HelloQuicProtocol,
        )
        print("Listening on https://0.0.0.0:4433")
        await asyncio.Event().wait()

    except (asyncio.CancelledError):
        print("\nApplication stopped manually!")


if __name__ == "__main__":
    asyncio.run(main())
