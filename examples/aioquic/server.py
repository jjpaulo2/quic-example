import asyncio

from aioquic.asyncio.server import serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.h3.events import HeadersReceived
from aioquic.quic.events import QuicEvent

from examples.settings import CERTIFY_PATH, KEY_PATH


# Custom QUIC protocol handler class
class HelloQuicProtocol(QuicConnectionProtocol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define the HTTP/3 connection client
        self._http = H3Connection(self._quic)

    # Handle QUIC events (default method from QuicConnectionProtocol)
    def quic_event_received(self, event: QuicEvent):

        # Iterate over HTTP/3 events
        for http_event in self._http.handle_event(event):
            
            # Handle only headers received events
            if isinstance(http_event, HeadersReceived):
                
                # Log the request headers
                print(http_event.headers)

                # Write the response headers
                self._http.send_headers(
                    stream_id=http_event.stream_id,
                    headers=[
                        (b':status', b'200'),
                        (b'content-type', b'text/plain')
                    ],
                )
                
                # Write the response body and end the stream
                self._http.send_data(
                    stream_id=http_event.stream_id,
                    data=b"hello world\n",
                    end_stream=True
                )

                # Optional, ensure pending data is sent
                self.transmit()
                

async def main():
    # Instantiate the QUIC server configuration
    config = QuicConfiguration(is_client=False, alpn_protocols=H3_ALPN)

    # Load the server certificate and private key
    config.load_cert_chain(certfile=CERTIFY_PATH, keyfile=KEY_PATH)
    
    try:
        # Start the QUIC server
        await serve(
            host="0.0.0.0",
            port=4433,
            configuration=config,
            create_protocol=HelloQuicProtocol,
        )

        # Log server start
        print("Listening on https://0.0.0.0:4433")
        
        # Wait for event loop events
        await asyncio.Event().wait()

    # Don't crash on manual stop (Ctrl+C)
    except (asyncio.CancelledError):
        print("\nApplication stopped manually!")


if __name__ == "__main__":
    # Running the main event loop
    asyncio.run(main())
