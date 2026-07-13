from .components import (
    Component, Text, Button, Switch, LongPress, DigitString,
    Input, Toggle, Slider, ProgressBar, DragBar, ScrollView, Image,
    TableView, Dialog, Spinner, TypewriterPanel, CountdownConfig, Html,
    StatusDot, CodeBlock, LogViewer, Keypad, Separator,
    Checkbox, Dropdown, Modal, LogGenerator, ChoiceGroup,
    AudioToggle, Preloader, StoryText,
)


class Panel:
    def __init__(self, panel_id, label=None):
        self.id = panel_id
        self.label = label or panel_id
        self.rows = [[]]
        self.typewriter_config = None
        self.countdown_config = None
        self.dialogs = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def _add(self, component):
        self.rows[-1].append(component)
        return component

    def row(self):
        if self.rows[-1]:
            self.rows.append([])
        return self

    def add_row(self, components):
        if self.rows[-1]:
            self.rows.append([])
        for c in components:
            self.rows[-1].append(c)
        self.rows.append([])
        return self

    def text(self, content="", **kwargs):
        return self._add(Text(content, **kwargs))

    def button(self, label="", **kwargs):
        return self._add(Button(label, **kwargs))

    def switch(self, label="", options=None, **kwargs):
        return self._add(Switch(label, options, **kwargs))

    def long_press(self, label="", **kwargs):
        return self._add(LongPress(label, **kwargs))

    def digit_string(self, length=4, **kwargs):
        return self._add(DigitString(length, **kwargs))

    def input(self, placeholder="", **kwargs):
        return self._add(Input(placeholder, **kwargs))

    def toggle(self, label="", **kwargs):
        return self._add(Toggle(label, **kwargs))

    def slider(self, label="", **kwargs):
        return self._add(Slider(label, **kwargs))

    def progress(self, value=0, max_val=100, label=""):
        return self._add(ProgressBar(value, max_val, label))

    def scroll_view(self, content="", height="200px"):
        return self._add(ScrollView(content, height))

    def image(self, src="", alt="", **kwargs):
        return self._add(Image(src, alt, **kwargs))

    def table(self, headers=None, rows=None):
        return self._add(TableView(headers, rows))

    def html(self, content=""):
        return self._add(Html(content))

    def dialog(self, dialog_id="", title="", message="", confirm_label="OK"):
        d = Dialog(dialog_id, title, message, confirm_label)
        self.dialogs.append(d)
        return self._add(d)

    def spinner(self, label=""):
        return self._add(Spinner(label))

    def status_dot(self, label="", color="green"):
        return self._add(StatusDot(label, color))

    def code_block(self, code="", max_height=None):
        return self._add(CodeBlock(code, max_height))

    def log_viewer(self, lines=None, max_lines=50):
        return self._add(LogViewer(lines, max_lines))

    def keypad(self, target_id=None):
        return self._add(Keypad(target_id))

    def separator(self):
        return self._add(Separator())

    def checkbox(self, label="", checked=False):
        return self._add(Checkbox(label, checked))

    def dropdown(self, label="", options=None, default_index=0):
        return self._add(Dropdown(label, options, default_index))

    def modal(self, modal_id="", title="", content_html=""):
        return self._add(Modal(modal_id, title, content_html))

    def dragbar(self, value=0, label=""):
        return self._add(DragBar(value, label))

    def log_generator(self, lines=None, max_lines=50, speed=50):
        return self._add(LogGenerator(lines, max_lines, speed))

    def choice_group(self, choices=None):
        return self._add(ChoiceGroup(choices))

    def audio_toggle(self, initially_muted=False):
        return self._add(AudioToggle(initially_muted))

    def preloader(self, stages=None, auto_start=True):
        return self._add(Preloader(stages, auto_start))

    def story_text(self, lines=None, auto_advance=True):
        return self._add(StoryText(lines, auto_advance))

    def set_typewriter(self, secret_words=None, prompt="Press any letter key..."):
        self.typewriter_config = TypewriterPanel(secret_words, prompt)
        return self

    def set_countdown(self, target_date, modes=None, label=""):
        self.countdown_config = CountdownConfig(target_date, modes, label)
        return self

    def get_all_callbacks(self):
        cbs = {}
        for row in self.rows:
            for comp in row:
                if comp.callback_id and comp._python_callback:
                    cbs[comp.callback_id] = comp._python_callback
                if hasattr(comp, "dialogs"):
                    for d in comp.dialogs:
                        if d.callback_id and d._python_callback:
                            cbs[d.callback_id] = d._python_callback
        return cbs
