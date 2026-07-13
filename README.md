# CTUI — CARNIVAL Terminal UI

A Gradio-style Python library for building retro terminal UIs in the CARNIVAL aesthetic: black background, pixel font, keyboard-driven cursor navigation, mouse snapping, and a full component system.

## Quick Start

```python
from CTUI import TerminalApp

app = TerminalApp("My App")

with app.panel("main") as p:
    p.text("Welcome to CTUI")
    p.button("Settings", target="settings")
    p.long_press("Submit").on_activate(lambda v: print("done"))

with app.panel("settings") as p:
    p.switch("Sound", ["Off", "On", "Mute"])
    p.slider("Volume", 0, 100, 50)
    p.button("Back", target="main")

app.run()          # browser at http://127.0.0.1:5051
# app.launch()     # pywebview desktop window
# app.save("out.html")  # static HTML
```

## Install

```bash
pip install flask pywebview   # runtime dependencies
```

Run the demo:
```bash
python -m CTUI.demo web       # browser
python -m CTUI.demo lan       # LAN access
```

## Components

| Component | API | Description |
|---|---|---|
| **Text** | `p.text("content")` | Static text, skipped by cursor |
| **Button** | `p.button("label", target="panel")` | Clickable, switches panels or triggers callbacks |
| **Switch** | `p.switch("label", ["A","B","C"])` | Cycles options on Enter |
| **Toggle** | `p.toggle("label")` | ON/OFF binary switch |
| **Checkbox** | `p.checkbox("label")` | `[x]` style checkbox |
| **Dropdown** | `p.dropdown("label", ["A","B"])` | Cycles with `[option]` display |
| **LongPress** | `p.long_press("label")` | Hold Enter 2s to activate, charge bar animation |
| **Input** | `p.input("placeholder")` | Text input, Enter to submit |
| **DigitString** | `p.digit_string(6)` | Digit-by-digit editor, arrow keys + number keys |
| **Slider** | `p.slider("label", 0, 100, 50)` | Adjustable value, Enter to edit, arrows to change |
| **DragBar** | `p.dragbar(42, "label")` | Click/drag bar, keyboard-only in cursor mode |
| **ProgressBar** | `p.progress(65, 100)` | Read-only progress indicator |
| **LogGenerator** | `p.log_generator(lines, speed)` | Auto-scrolling boot log animation |
| **CommandConsole** | `p.command_console(prompts, parser)` | Command-line interface with parsing engine |
| **Keypad** | `p.keypad()` | On-screen numeric keypad, arrow keys + Enter |
| **MemoryMatch** | `p.memory_match(rows, cols, pairs, timer)` | Memory card matching game |
| **ChoiceGroup** | `p.choice_group(["A","B"])` | Interactive choice buttons with keyboard navigation |
| **StoryText** | `p.story_text(lines)` | Typewriter novel reader, char-by-char reveal |
| **ScrollPanel** | `p.scroll_panel(components, height)` | Auto-scrolling container for overflow content |
| **Table** | `p.table(headers, rows)` | Data table display |
| **CodeBlock** | `p.code_block("code")` | Pre-formatted code display |
| **LogViewer** | `p.log_viewer(["line1"])` | Static log viewer |
| **ScrollView** | `p.scroll_view("content")` | Scrollable text area |
| **Image** | `p.image("src.png")` | Pixel-art image display |
| **StatusDot** | `p.status_dot("Online", "green")` | Colored indicator with pulse animation |
| **GlitchText** | `p.glitch_text("CLASSIFIED")` | Text with glitch/skew animation |
| **WebGLShader** | `p.webgl_shader(fragment_src)` | Full-screen custom GLSL shader canvas |
| **Separator** | `p.separator()` | Horizontal divider |
| **Spinner** | `p.spinner("Loading")` | CSS-animated loading indicator |
| **AudioToggle** | `p.audio_toggle()` | Mute/unmute button |
| **Dialog** | `p.dialog("id", "title", "msg")` | Overlay dialog with backdrop |
| **Modal** | `p.modal("id", "title", "html")` | Overlay modal with custom content |
| **Typewriter** | `p.set_typewriter(secrets)` | Panel-level fullscreen char display + word matching |
| **Countdown** | `p.set_countdown("2026-02-17T00:00:00")` | Panel-level real-time countdown |
| **Preloader** | `p.preloader(stages)` | Boot sequence progress bar |

## Colors

Bar-type components (slider, progress, dragbar) accept a `color` parameter:

```python
p.slider("Volume", color="white")    # default: white
p.progress(50, color="teal")         # teal/green
p.dragbar(30, color="yellow")        # yellow
p.slider("Level", color="red")       # red
```

## Callbacks

Attach Python callbacks to interactive components:

```python
def on_click(val):
    print(f"Clicked with value: {val}")
    return {"action": "set-text", "target": "status", "value": "done"}

p.button("Go").on_activate(on_click)
p.switch("Mode").on_activate(on_click)
p.input("Name").on_submit(on_click)
p.long_press("Hold").on_activate(on_click)
```

Return a dict to trigger frontend actions:

| Action | Effect |
|---|---|
| `{"action": "set-text", "target": "id", "value": "..."}` | Set element textContent |
| `{"action": "set-text", ..., "show": "#btn-id"}` | Also reveal a hidden element |
| `{"action": "set-text", ..., "status": "#el", "statusValue": "..."}` | Update all `[id^="status-s"]` elements |
| `{"action": "switch-panel", "target": "panel-id"}` | Navigate to panel |
| `{"action": "show-dialog", "dialogId": "id"}` | Open dialog |
| `{"action": "hide-dialog", "dialogId": "id"}` | Close dialog |
| `{"action": "set-progress", "target": "id", "value": 50, "max": 100}` | Update progress bar |
| `{"action": "set-digit", "target": "id", "value": "1234"}` | Fill digit string |
| `{"action": "set-visible", "target": "id"}` | Toggle `data-visible` attribute |

## Keyboard Navigation

| Key | Action |
|---|---|
| `↑ ↓ ← →` | Move cursor between components |
| `Enter` | Activate component / confirm |
| `Enter` (hold) | Long-press activation (2s) |
| `Escape` | Close dialog / exit edit mode / skip story typing |
| `↑ ↓` (on StoryText) | Scroll story content when not complete |
| `↑ ↓` (on ChoiceGroup) | Navigate choice options |
| `↑ ↓ ← →` (on Keypad) | Navigate keypad keys |

## Mouse

- Default cursor is hidden; a retro block cursor (`#terminal-cursor`) follows the pointer
- Snaps to components within 30px
- Click activates the component (same as keyboard Enter)
- 3s idle: mouse cursor fades out over 0.4s, keyboard cursor fades in
- Mouse move: keyboard cursor hides immediately

## Server

```python
app.run()                        # localhost only
app.run(allow_lan=True)          # bind 0.0.0.0, show LAN address
app.launch()                     # pywebview desktop window
```

## License

MIT
