import json
import uuid

_next_cb_id = 0

def _new_callback_id():
    global _next_cb_id
    _next_cb_id += 1
    return f"cb_{_next_cb_id - 1}"


class Component:
    type = None
    tag = "span"
    is_selectable = True
    is_text = False

    def __init__(self):
        self.attrs = {}
        self.style = {}
        self.content = ""
        self.callback_id = None
        self._python_callback = None
        self._extra_classes = set()

    def add_class(self, cls):
        self._extra_classes.add(cls)
        return self

    def set_style(self, **kwargs):
        self.style.update(kwargs)
        return self

    def set_attr(self, key, value):
        self.attrs[key] = value
        return self

    def on_activate(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        self.attrs["data-action"] = "callback"
        return self

    def _render_attrs(self):
        parts = []
        for k, v in self.attrs.items():
            if v is True:
                parts.append(k)
            elif v is not None and v is not False:
                v = str(v).replace('"', "&quot;")
                parts.append(f'{k}="{v}"')
        return " ".join(parts)

    def _render_style(self):
        if not self.style:
            return ""
        inline = "; ".join(f"{k}: {v}" for k, v in self.style.items())
        return f' style="{inline}"'

    def render(self):
        cls = "terminal-component"
        if self._extra_classes:
            cls += " " + " ".join(self._extra_classes)
        data_type = ""
        if self.type:
            data_type = f' data-type="{self.type}"'
        attrs = self._render_attrs()
        style = self._render_style()
        if attrs:
            return f'<{self.tag} class="{cls}"{data_type} {attrs}{style}>{self.content}</{self.tag}>'
        return f'<{self.tag} class="{cls}"{data_type}{style}>{self.content}</{self.tag}>'


class Text(Component):
    is_selectable = False
    is_text = True

    def __init__(self, content="", font_size=None, font_family=None, opacity=0.7):
        super().__init__()
        self.type = "text"
        self.tag = "span"
        self.content = content
        if font_size:
            self.attrs["data-font-size"] = font_size
        if font_family:
            self.attrs["data-font-family"] = font_family
        self.style["opacity"] = str(opacity)


class Button(Component):
    def __init__(self, label="", target=None, action=None):
        super().__init__()
        self.tag = "button"
        self.content = label
        if target:
            self.attrs["data-action"] = "switch-panel"
            self.attrs["data-target"] = target
        elif action:
            self.attrs["data-action"] = action


class Switch(Component):
    def __init__(self, label="", options=None, current_index=0, action=None):
        super().__init__()
        self.tag = "button"
        self.type = "switch"
        self._label = label
        self._options = options or ["On", "Off"]
        self._current_index = current_index
        self.attrs["data-label"] = label
        self.attrs["data-options"] = ",".join(self._options)
        self.attrs["data-current-index"] = str(current_index)
        self.content = label + self._options[current_index]
        if action:
            self.attrs["data-action"] = action


class LongPress(Component):
    def __init__(self, label="", duration=2000, action=None):
        super().__init__()
        self.tag = "button"
        self.type = "long-press"
        self.content = label
        self.attrs["data-duration"] = str(duration)
        if action:
            self.attrs["data-action"] = action

    def on_activate(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        self.attrs["data-action"] = "callback"
        return self


class DigitString(Component):
    def __init__(self, length=4, action=None):
        super().__init__()
        self.tag = "div"
        self.type = "digit-string"
        self.attrs["data-length"] = str(length)
        digits = "".join(
            '<span class="digit-char">_</span>' for _ in range(length)
        )
        self.content = digits
        self._panel_id = None
        if action:
            self.attrs["data-action"] = action

    def on_activate(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        self.attrs["data-action"] = "callback"
        return self


class Input(Component):
    def __init__(self, placeholder="", value=""):
        super().__init__()
        self.tag = "input"
        self.attrs["type"] = "text"
        self.attrs["placeholder"] = placeholder
        self.attrs["value"] = value
        self.content = ""

    def on_submit(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        self.attrs["data-action"] = "callback"
        return self

    def render(self):
        cls = "terminal-component"
        if self.type:
            cls += f' data-type="{self.type}"'
        attrs = self._render_attrs()
        style = self._render_style()
        return f'<{self.tag} class="{cls}" {attrs}{style}>'


class Toggle(Component):
    def __init__(self, label="", checked=False, action=None):
        super().__init__()
        self.tag = "button"
        self.type = "toggle"
        self._label = label
        self.attrs["data-label"] = label
        self.attrs["data-checked"] = "true" if checked else "false"
        self.content = label + ("ON" if checked else "OFF")
        if action:
            self.attrs["data-action"] = action

    def on_activate(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        self.attrs["data-action"] = "callback"
        return self


class Slider(Component):
    def __init__(self, label="", min_val=0, max_val=100, value=50, step=1, color=None):
        super().__init__()
        self.tag = "div"
        self.type = "slider"
        self._label = label
        self.attrs["data-min"] = str(min_val)
        self.attrs["data-max"] = str(max_val)
        self.attrs["data-value"] = str(value)
        self.attrs["data-step"] = str(step)
        if color:
            self.attrs["data-color"] = color
        color_map = {"white": "#fff", "teal": "#2a9d8f", "yellow": "#e9c46a", "red": "#e76f51"}
        bar_color = color_map.get(color, "#fff" if color is None else color)
        pct = ((value - min_val) / (max_val - min_val)) * 100 if max_val > min_val else 0
        self.content = (
            f'<span class="slider-label">{label}</span>'
            f'<span class="slider-value">{value}</span>'
            f'<span class="slider-track" style="--bar-color:{bar_color}">'
            f'<span class="slider-fill" style="width:{pct:.1f}%"></span>'
            f"</span>"
            f'<button class="slider-btn slider-dec" data-action="slider-dec">-</button>'
            f'<button class="slider-btn slider-inc" data-action="slider-inc">+</button>'
        )

    def on_change(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        return self


class ProgressBar(Component):
    is_selectable = False
    is_text = True

    def __init__(self, value=0, max_val=100, label="", color=None):
        super().__init__()
        self.tag = "div"
        self.type = "progress"
        self.attrs["data-value"] = str(value)
        self.attrs["data-max"] = str(max_val)
        if color:
            self.attrs["data-color"] = color
        color_map = {"white": "#fff", "teal": "#2a9d8f", "yellow": "#e9c46a", "red": "#e76f51"}
        bar_color = color_map.get(color, "#2a9d8f" if color is None else color)
        pct = (value / max_val) * 100 if max_val > 0 else 0
        self.content = (
            f'<span class="progress-label">{label}</span>'
            f'<span class="progress-track" style="--bar-color:{bar_color}">'
            f'<span class="progress-fill" style="width:{pct:.1f}%"></span>'
            f"</span>"
            f'<span class="progress-text">{pct:.0f}%</span>'
        )


class ScrollView(Component):
    is_selectable = False
    is_text = True

    def __init__(self, content="", height="200px"):
        super().__init__()
        self.tag = "div"
        self.type = "scroll-view"
        self.style["height"] = height
        self.content = f'<pre class="scroll-content">{content}</pre>'


class Image(Component):
    is_selectable = False
    is_text = True

    def __init__(self, src="", alt="", width=None, height=None):
        super().__init__()
        self.tag = "div"
        self.type = "image"
        w = f' width="{width}"' if width else ""
        h = f' height="{height}"' if height else ""
        self.content = f'<img src="{src}" alt="{alt}"{w}{h} class="terminal-image">'


class TableView(Component):
    is_selectable = False
    is_text = True

    def __init__(self, headers=None, rows=None):
        super().__init__()
        self.tag = "div"
        self.type = "table"
        headers = headers or []
        rows = rows or []
        hdr = (
            "<thead><tr>"
            + "".join(f"<th>{h}</th>" for h in headers)
            + "</tr></thead>"
        )
        bdy = "<tbody>"
        for row in rows:
            bdy += (
                "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
            )
        bdy += "</tbody>"
        self.content = f"<table>{hdr}{bdy}</table>"


class Dialog(Component):
    def __init__(self, dialog_id="", title="", message="", confirm_label="OK"):
        super().__init__()
        self.tag = "div"
        self.type = "dialog"
        self.attrs["data-dialog-id"] = dialog_id
        self.attrs["data-visible"] = "false"
        self.content = (
            f'<div class="dialog-backdrop" data-action="dialog-close" data-target="{dialog_id}"></div>'
            f'<div class="dialog-box">'
            f'<div class="dialog-title">{title}</div>'
            f'<div class="dialog-message">{message}</div>'
            f'<button class="terminal-component dialog-confirm" data-action="dialog-close" data-target="{dialog_id}">{confirm_label}</button>'
            f"</div>"
        )

    def render(self):
        cls = "terminal-component dialog-overlay"
        attrs = self._render_attrs()
        style = self._render_style()
        data_type = f' data-type="{self.type}"' if self.type else ""
        return f'<{self.tag} class="{cls}"{data_type} {attrs}{style}>{self.content}</{self.tag}>'


class Spinner(Component):
    is_selectable = False
    is_text = True

    def __init__(self, label=""):
        super().__init__()
        self.tag = "span"
        self.type = "spinner"
        self.content = f'<span class="spinner-anim">{label}</span>'


class TypewriterPanel:
    def __init__(self, secret_words=None, prompt="Press any letter key..."):
        self.secret_words = secret_words or {}
        self.prompt = prompt


class CountdownConfig:
    def __init__(self, target_date, modes=None, label=""):
        self.target_date = target_date
        self.modes = modes or ["standard", "timestamp"]
        self.label = label


class Html(Component):
    is_selectable = False
    is_text = True

    def __init__(self, html=""):
        super().__init__()
        self.tag = "div"
        self.type = "html"
        self.content = html


class StatusDot(Component):
    is_selectable = False
    is_text = True

    def __init__(self, label="", color="green"):
        super().__init__()
        self.tag = "span"
        self.type = "status"
        self.attrs["data-color"] = color
        self.content = f'<span class="dot" style="background:{color}"></span> {label}'


class CodeBlock(Component):
    is_selectable = False
    is_text = True

    def __init__(self, code="", max_height=None):
        super().__init__()
        self.tag = "pre"
        self.type = "code"
        if max_height:
            self.style["max-height"] = max_height
            self.style["overflow-y"] = "auto"
        self.content = code


class LogViewer(Component):
    is_selectable = False
    is_text = True

    def __init__(self, lines=None, max_lines=50):
        super().__init__()
        self.tag = "div"
        self.type = "log"
        self.attrs["data-max-lines"] = str(max_lines)
        lines = lines or []
        self.content = "<pre>" + "\n".join(lines) + "</pre>"


class Keypad(Component):
    def __init__(self, target_id=None):
        super().__init__()
        self.tag = "div"
        self.type = "keypad"
        if target_id:
            self.attrs["data-target"] = target_id
        keys = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["←", "0", "✓"],
        ]
        rows = ""
        for r in keys:
            cells = "".join(
                f'<button class="keypad-key" data-key="{k}">{k}</button>' for k in r
            )
            rows += f'<div class="keypad-row">{cells}</div>'
        self.content = rows

    def on_activate(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        self.attrs["data-action"] = "callback"
        return self


class Separator(Component):
    is_selectable = False
    is_text = True

    def __init__(self):
        super().__init__()
        self.tag = "div"
        self.type = "separator"
        self.content = "────────────────────"


class Checkbox(Component):
    def __init__(self, label="", checked=False):
        super().__init__()
        self.tag = "button"
        self.type = "checkbox"
        self.attrs["data-checked"] = "true" if checked else "false"
        mark = "[x]" if checked else "[ ]"
        self.content = mark + " " + label

    def on_activate(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        self.attrs["data-action"] = "callback"
        return self


class Dropdown(Component):
    def __init__(self, label="", options=None, default_index=0):
        super().__init__()
        self.tag = "button"
        self.type = "dropdown"
        options = options or ["--"]
        self.attrs["data-label"] = label
        self.attrs["data-options"] = ",".join(options)
        self.attrs["data-current-index"] = str(default_index)
        self.content = f"{label}[{options[default_index]}]"

    def on_activate(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        self.attrs["data-action"] = "callback"
        return self


class Modal(Component):
    is_selectable = False
    is_text = True

    def __init__(self, modal_id="", title="", content_html=""):
        super().__init__()
        self.tag = "div"
        self.type = "modal"
        self.attrs["data-modal-id"] = modal_id
        self.attrs["data-visible"] = "false"
        self.content = (
            f'<div class="modal-backdrop" data-action="modal-close" data-target="{modal_id}"></div>'
            f'<div class="modal-box">'
            f'<div class="modal-title">{title}</div>'
            f'<div class="modal-body">{content_html}</div>'
            f'<button class="terminal-component modal-confirm" data-action="modal-close" data-target="{modal_id}">OK</button>'
            f"</div>"
        )

    def render(self):
        cls = "terminal-component modal-overlay"
        attrs = self._render_attrs()
        style = self._render_style()
        data_type = f' data-type="{self.type}"' if self.type else ""
        return f'<{self.tag} class="{cls}"{data_type} {attrs}{style}>{self.content}</{self.tag}>'


class DragBar(Component):
    is_selectable = True

    def __init__(self, value=0, label="", color=None):
        super().__init__()
        self.tag = "div"
        self.type = "dragbar"
        self.attrs["data-value"] = str(value)
        if color:
            self.attrs["data-color"] = color
        color_map = {"white": "#fff", "teal": "#2a9d8f", "yellow": "#e9c46a", "red": "#e76f51"}
        bar_color = color_map.get(color, "#2a9d8f" if color is None else color)
        self.content = (
            f'<span class="dragbar-label">{label}</span>'
            f'<span class="dragbar-track" style="--bar-color:{bar_color}">'
            f'<span class="dragbar-fill" style="width:{value}%"></span>'
            f'<span class="dragbar-thumb" style="left:{value}%"></span>'
            f"</span>"
            f'<span class="dragbar-value">{value}%</span>'
        )

    def on_change(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        return self


class LogGenerator(Component):
    is_selectable = False
    is_text = True

    def __init__(self, lines=None, max_lines=50, speed=50):
        super().__init__()
        self.tag = "div"
        self.type = "log-gen"
        self.attrs["data-max-lines"] = str(max_lines)
        self.attrs["data-speed"] = str(speed)
        import json as _j
        self.attrs["data-lines"] = _j.dumps(lines or [
            "INITIALIZING SYSTEM...",
            "LOADING MEMORY FRAGMENTS...",
            "SYNCHRONIZING NEURAL LINK...",
            "READY.",
        ])


class ChoiceGroup(Component):
    def __init__(self, choices=None):
        super().__init__()
        self.tag = "div"
        self.type = "choice-group"
        choices = choices or ["Continue"]
        self.attrs["data-choices"] = ",".join(str(c) for c in choices)
        btns = "".join(
            f'<button class="choice-btn terminal-component" data-choice-index="{i}">{c}</button>'
            for i, c in enumerate(choices)
        )
        self.content = btns

    def on_choose(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        return self


class AudioToggle(Component):
    def __init__(self, initially_muted=False):
        super().__init__()
        self.tag = "button"
        self.type = "audio-toggle"
        self.attrs["data-muted"] = "true" if initially_muted else "false"
        self.content = "[🔊]" if not initially_muted else "[🔇]"

    def on_toggle(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        return self


class Preloader(Component):
    is_selectable = False
    is_text = True

    def __init__(self, stages=None, auto_start=True):
        super().__init__()
        self.tag = "div"
        self.type = "preloader"
        import json as _j
        self.attrs["data-stages"] = _j.dumps(stages or [
            {"pct": 25, "label": "INITIALIZING..."},
            {"pct": 50, "label": "LOADING ASSETS..."},
            {"pct": 75, "label": "SYNCHRONIZING..."},
            {"pct": 100, "label": "READY."},
        ])
        self.attrs["data-auto-start"] = "true" if auto_start else "false"
        self.content = (
            '<div class="preloader-label">INITIALIZING...</div>'
            '<div class="preloader-track"><div class="preloader-fill"></div></div>'
        )

    def on_complete(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        return self


class StoryText(Component):
    is_selectable = False
    is_text = True

    def __init__(self, lines=None, auto_advance=True):
        super().__init__()
        self.tag = "div"
        self.type = "story-text"
        import json as _j
        self.attrs["data-lines"] = _j.dumps(lines or [
            {"speaker": "??", "text": "Hello..."},
            {"text": "A voice echoes in the dark."},
        ])
        self.attrs["data-auto"] = "true" if auto_advance else "false"
        self.content = (
            '<div class="story-scroll"><div class="story-lines"></div></div>'
            '<div class="story-continue">CLICK TO CONTINUE</div>'
        )

    def on_line(self, fn):
        self._python_callback = fn
        self.callback_id = _new_callback_id()
        self.attrs["data-callback-id"] = self.callback_id
        return self


class ScrollPanel(Component):
    is_selectable = False
    is_text = True

    def __init__(self, components=None, height="120px"):
        super().__init__()
        self.tag = "div"
        self.type = "scroll-panel"
        self.style["height"] = height
        self._children = components or []
        rendered = ""
        for c in self._children:
            rendered += f'<div class="component-row">{c.render()}</div>'
        self.content = rendered

    def add(self, *components):
        for c in components:
            self._children.append(c)
            self.content += f'<div class="component-row">{c.render()}</div>'
        return self
