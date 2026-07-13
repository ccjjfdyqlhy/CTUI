import os
import json
import socket
import threading

from flask import Flask, send_from_directory, request, jsonify

from .templates import build_html


def _get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.254.254.254", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def _print_urls(host, port):
    if host == "0.0.0.0":
        lan = _get_lan_ip()
        print(f" * Local:   http://127.0.0.1:{port}")
        print(f" * LAN:     http://{lan}:{port}")
    else:
        print(f" * URL:     http://{host}:{port}")


class TerminalServer:
    def __init__(self, app, host="127.0.0.1", port=5051, debug=False):
        self._app_obj = app
        self.host = host
        self.port = port
        self.debug = debug
        self._flask = Flask(__name__)
        self._callbacks = {}
        self._assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        self._setup_routes()

    def _setup_routes(self):
        flask_app = self._flask
        callbacks = self._callbacks
        assets_dir = self._assets_dir
        app_obj = self._app_obj

        for cb_id, fn in app_obj.get_all_callbacks().items():
            callbacks[cb_id] = fn

        @flask_app.route("/")
        def index():
            html = build_html(app_obj)
            return html

        @flask_app.route("/assets/<path:path>")
        def serve_asset(path):
            return send_from_directory(assets_dir, path)

        @flask_app.route("/api/callback/<cb_id>", methods=["POST"])
        def handle_callback(cb_id):
            if cb_id not in callbacks:
                return jsonify({"error": "callback not found"}), 404
            data = request.get_json(silent=True) or {}
            try:
                fn = callbacks[cb_id]
                result = fn(data.get("value"))
                if result is None:
                    return jsonify({"status": "ok"})
                if isinstance(result, dict):
                    return jsonify(result)
                return jsonify({"status": "ok", "value": str(result)})
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @flask_app.route("/api/panels", methods=["GET"])
        def list_panels():
            return jsonify([p.id for p in app_obj.panels])

        @flask_app.route("/api/close", methods=["POST"])
        def close():
            import webview
            try:
                webview.windows[0].destroy()
            except Exception:
                pass
            return jsonify({"status": "ok"})

    def run(self, open_browser=False, use_webview=False):
        if use_webview:
            self._run_webview()
        else:
            self._run_flask(open_browser)

    def _run_flask(self, open_browser):
        if open_browser:
            import webbrowser
            url = f"http://127.0.0.1:{self.port}" if self.host == "0.0.0.0" else f"http://{self.host}:{self.port}"
            webbrowser.open(url)
        print(f" * CARNIVAL Terminal running (host={self.host})")
        _print_urls(self.host, self.port)
        self._flask.run(host=self.host, port=self.port, debug=self.debug, threaded=True)

    def _run_webview(self):
        import webview
        t = threading.Thread(target=lambda: self._flask.run(
            host=self.host, port=self.port, debug=self.debug, threaded=True
        ))
        t.daemon = True
        t.start()
        url = f"http://127.0.0.1:{self.port}" if self.host == "0.0.0.0" else f"http://{self.host}:{self.port}"
        print(f" * CARNIVAL Terminal running (webview)")
        _print_urls(self.host, self.port)
        webview.create_window(
            title=self._app_obj.title,
            url=url,
            width=800, height=600, resizable=True,
            min_size=(800, 600),
        )
        webview.start(debug=self.debug)
