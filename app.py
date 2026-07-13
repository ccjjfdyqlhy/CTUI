import os

from .panel import Panel
from .server import TerminalServer
from .templates import build_html


class TerminalApp:
    def __init__(self, title="CARNIVAL Terminal", font_size=16,
                 long_press_duration=2000, default_panel=None,
                 assets_url=None, api_base="/api"):
        self.title = title
        self.font_size = font_size
        self.long_press_duration = long_press_duration
        self.default_panel = default_panel or "panel-main"
        self.assets_url = assets_url or ""
        self.api_base = api_base
        self.panels = []
        self.dialogs = []
        self._current_panel = None
        self._server = None

    def set_title(self, title):
        self.title = title
        return self

    def panel(self, panel_id, label=None):
        p = Panel(panel_id, label or panel_id)
        self.panels.append(p)
        self._current_panel = p
        return p

    def add_panel(self, panel):
        self.panels.append(panel)
        self._current_panel = panel
        return panel

    def get_panel(self, panel_id):
        for p in self.panels:
            if p.id == panel_id:
                return p
        return None

    def get_all_callbacks(self):
        cbs = {}
        for p in self.panels:
            cbs.update(p.get_all_callbacks())
        return cbs

    def build_html(self):
        return build_html(self)

    def save_html(self, filepath):
        html = self.build_html()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        return filepath

    def _make_server(self, host="127.0.0.1", port=5051, debug=False):
        if self._server is None:
            self._server = TerminalServer(self, host=host, port=port, debug=debug)
        return self._server

    def run(self, host="127.0.0.1", port=5051, debug=False, open_browser=False, allow_lan=False):
        if allow_lan:
            host = "0.0.0.0"
        server = self._make_server(host, port, debug)
        server.run(open_browser=open_browser, use_webview=False)

    def launch(self, host="127.0.0.1", port=5051, debug=False, allow_lan=False):
        if allow_lan:
            host = "0.0.0.0"
        server = self._make_server(host, port, debug)
        server.run(use_webview=True)

    def serve(self, host="127.0.0.1", port=5051, debug=False, allow_lan=False):
        if allow_lan:
            host = "0.0.0.0"
        self.run(host=host, port=port, debug=debug, allow_lan=False)
