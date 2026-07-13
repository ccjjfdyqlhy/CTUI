import os
import json

_templates_dir = os.path.dirname(os.path.abspath(__file__))

files_css = ["base.css", "components.css", "overlays.css"]

files_js = ["terminal.js"]

files_js_order = {name: i for i, name in enumerate(files_js)}


def _read(filename):
    with open(os.path.join(_templates_dir, filename), "r", encoding="utf-8") as f:
        return f.read()


def build_css():
    return "\n".join(_read(f) for f in files_css)


def build_js():
    return "\n".join(_read(f) for f in files_js)


CSS = build_css()
JS_TERMINAL = build_js()


def render_panels_html(panels, dialogs):
    parts = []
    overlays = []
    for panel in panels:
        p_id = panel.id
        p_attrs = f' id="{p_id}" class="panel"'
        behavior_parts = []
        if panel.typewriter_config:
            behavior_parts.append('data-behavior="typewriter"')
            behavior_parts.append(
                'data-typewriter-prompt="' + panel.typewriter_config.prompt.replace('"', '&quot;') + '"'
            )
            if panel.typewriter_config.secret_words:
                behavior_parts.append(
                    'data-secret-words=\'' + json.dumps(panel.typewriter_config.secret_words, ensure_ascii=False) + '\''
                )
        if panel.countdown_config:
            behavior_parts.append('data-behavior="countdown"')
            behavior_parts.append(
                'data-target-date="' + panel.countdown_config.target_date + '"'
            )
            behavior_parts.append('data-countdown-mode="standard"')
        if behavior_parts:
            p_attrs += " " + " ".join(behavior_parts)

        parts.append(f"<div{p_attrs}>")
        parts.append('<div class="component-container">')
        parts.append('<div class="cursor-highlight keyboard-cursor"></div>')
        for row in panel.rows:
            if not row:
                continue
            parts.append('<div class="component-row">')
            for comp in row:
                if hasattr(comp, 'type') and comp.type in ('dialog', 'modal'):
                    overlays.append(comp.render())
                else:
                    parts.append(comp.render())
            parts.append("</div>")
        parts.append("</div></div>")
    return "\n".join(parts), "\n".join(overlays)


def render_typewriter_elements():
    return (
        '<div id="typewriter-large-char-display"></div>\n'
        '<div id="typewriter-message-display" class="typewriter-message"></div>'
    )


def build_html(app):
    has_typewriter = any(p.typewriter_config for p in app.panels)
    has_countdown = any(p.countdown_config for p in app.panels)

    panels_html, overlays = render_panels_html(app.panels, app.dialogs)
    tw_elements = render_typewriter_elements() if has_typewriter else ""

    font_url = app.assets_url + "fonts/LanaPixel.ttf" if app.assets_url else "assets/fonts/LanaPixel.ttf"

    config_json = json.dumps({
        "defaultPanel": app.default_panel,
        "longPressDuration": app.long_press_duration,
        "apiBase": app.api_base,
    })

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{app.title}</title>
<style>
@font-face{{font-family:'LanaPixel';src:url('{font_url}') format('truetype')}}
{CSS}
</style>
</head>
<body>
<div id="terminal">
<div class="terminal-content">
{panels_html}
{tw_elements}
</div>
{overlays}
</div>
<script>
var TERMINAL_CONFIG = {config_json};
{JS_TERMINAL}
document.addEventListener('DOMContentLoaded', function() {{
    new CARNIVALTerminal(TERMINAL_CONFIG);
}});
</script>
</body>
</html>"""
