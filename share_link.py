"""Launch the Dash app locally and expose a temporary shareable link via ngrok."""

import threading
import time
import webbrowser

from pyngrok import ngrok

from app import app


PORT = 8050


def _run_server():
    app.run_server(host="0.0.0.0", port=PORT, debug=False)


def main():
    server_thread = threading.Thread(target=_run_server, daemon=True)
    server_thread.start()

    # Allow the server to start before creating the tunnel
    time.sleep(1.5)
    public_tunnel = ngrok.connect(PORT, "http")
    public_url = public_tunnel.public_url

    print("Your app is now publicly accessible:")
    print(public_url)

    webbrowser.open_new(public_url)
    server_thread.join()


if __name__ == "__main__":
    main()
