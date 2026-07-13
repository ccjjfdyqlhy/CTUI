"""Demo: showcases every component of the CARNIVAL Terminal library."""
from CTUI import TerminalApp

app = TerminalApp(title="CARNIVAL Terminal — Demo")

# ── main ────────────────────────────────────────────────────
with app.panel("main") as p:
    p.text("█ CARNIVAL Terminal Library █", font_size="22px")
    p.text("A Gradio-like terminal UI library.", font_size="12px")
    p.row()
    p.button("📋 Components", target="panel-components")
    p.button("⚙ Settings", target="panel-settings")
    p.button("⌨ Typewriter", target="panel-typewriter")
    p.button("⏱ Countdown", target="panel-countdown")
    p.button("📁 ScrollView", target="panel-scroll")
    p.button("📊 Table", target="panel-table")
    p.button("🗂 Dialog", target="panel-dialog")
    p.button("🧩 More", target="panel-more")
    p.row()
    p.long_press("⏻ Long-press to shutdown", duration=2000,
                 action="callback").on_activate(
        lambda v: {"action": "show-dialog", "dialogId": "dlg-shutdown"}
    )

# ── Components ──────────────────────────────────────────────
def on_toggle(val):
    return {"action": "set-text", "target": "toggle-status",
            "value": f"Toggle: {'ON' if val == 'true' else 'OFF'}"}

def on_switch(val):
    return {"action": "set-text", "target": "switch-status",
            "value": f"Switch: {val}"}

def on_slider(val):
    return {"action": "set-text", "target": "slider-status",
            "value": f"Slider: {val}"}

def on_submit(val):
    return {"action": "set-text", "target": "input-status",
            "value": f"You typed: {val}"}

def on_digit(val):
    return {"action": "set-text", "target": "digit-status",
            "value": f"Digits: {val}"}

with app.panel("panel-components") as p:
    p.text("▸ Interactive Components")
    p.row()
    p.toggle("Enable: ", checked=False).on_activate(on_toggle)
    p.text("", font_size="12px")  # spacer
    p.row()
    p.text("Toggle status: ", font_size="12px")
    p.text("—", font_size="12px").set_attr("id", "toggle-status")
    p.row()
    p.switch("Sound: ", ["Off", "On", "Mute"]).on_activate(on_switch)
    p.text("Switch status: ", font_size="12px")
    p.text("—", font_size="12px").set_attr("id", "switch-status")
    p.row()
    p.slider("Volume: ", min_val=0, max_val=100, value=50).on_change(on_slider)
    p.text("Slider status: ", font_size="12px")
    p.text("—", font_size="12px").set_attr("id", "slider-status")
    p.row()
    p.digit_string(length=6).on_activate(on_digit)
    p.text("Digit status: ", font_size="12px")
    p.text("—", font_size="12px").set_attr("id", "digit-status")
    p.row()
    p.input(placeholder="Type something...").on_submit(on_submit)
    p.text("Input status: ", font_size="12px")
    p.text("—", font_size="12px").set_attr("id", "input-status")
    p.row()
    p.progress(value=65, max_val=100, label="Progress:")
    p.row()
    p.dragbar(value=42, label="DragBar:")
    p.row()
    p.spinner("Loading...")
    p.row()
    p.button("← Back", target="main")

# ── Settings ────────────────────────────────────────────────
current_font = ["LanaPixel", "Courier New", "Verdana"]

def on_font_change(val):
    idx = int(val) if val and val.isdigit() else 0
    font = current_font[idx] if idx < len(current_font) else current_font[0]
    return {"action": "set-text", "target": "font-status",
            "value": f"Font: {font}"}

with app.panel("panel-settings") as p:
    p.text("▸ Settings")
    p.row()
    p.switch("Font: ", current_font).on_activate(on_font_change)
    p.text("Font status: ", font_size="12px")
    p.text("—", font_size="12px").set_attr("id", "font-status")
    p.row()
    p.text("Font size:", font_size="12px")
    p.button("−", action="change-font-size").set_attr("data-value", "decrease")
    p.button("+", action="change-font-size").set_attr("data-value", "increase")
    p.button("← Back", target="main")

# ── Typewriter ──────────────────────────────────────────────
with app.panel("panel-typewriter") as p:
    p.set_typewriter(
        secret_words={
            "hello": "Hello, visitor!",
            "carnival": "The carnival never ends...",
            "help": "I am just a terminal.",
            "secret": "Some secrets are better left unknown.",
            "goodbye": "Farewell, traveler.",
            "password": "Access denied.",
            "open": " sesame!",
            "truth": "You are not alone.",
            "system": "System status: NOMINAL.",
            "reboot": "Reboot request rejected.",
        },
        prompt="Press any letter key to type...",
    )
    p.button("← Back", target="main")

# ── Countdown ───────────────────────────────────────────────
with app.panel("panel-countdown") as p:
    p.set_countdown(
        target_date="2026-02-17T00:00:00",
        label="Distance to Spring Festival 2026",
    )
    p.text("▸ Countdown")
    p.row()
    p.text("Target: 2026-02-17 (Chinese New Year)", font_size="12px")
    p.text("", font_size="48px").add_class("countdown-large-text").set_attr("data-countdown-display", "").set_attr("id", "countdown-display")
    p.row()
    p.switch("Mode: ", ["Standard", "Timestamp"],
             action="toggle-countdown-mode")
    p.row()
    p.button("← Back", target="main")

# ── ScrollView ──────────────────────────────────────────────
long_text = """MEMORY FRAGMENT #7C4
─────────────────
Date: 2024-12-31 23:58:47
Subject: Consciousness Link Experiment

The CARNIVAL system is initializing.
Eight subjects are connected to the matrix.
Neural synchronization at 97.4%.

───
Warning: Anomaly detected in Subject_04's memory partition.
Temporal distortion: +3.7 seconds.
Recommendation: Abort and restart.

───
The link cannot be broken.
System crash imminent.
Memory fragmentation in progress.

───
If you are reading this, you are one of the seven.
Find the fragments. Reconstruct the truth.
Before it is too late.

───
[END OF FRAGMENT]"""

with app.panel("panel-scroll") as p:
    p.text("▸ Scrollable Content")
    p.row()
    p.scroll_view(long_text, height="300px")
    p.row()
    p.button("← Back", target="main")

# ── Table ───────────────────────────────────────────────────
with app.panel("panel-table") as p:
    p.text("▸ Data Table")
    p.row()
    p.table(
        headers=["Subject", "Layer", "Status", "Fragments"],
        rows=[
            ["Subject_01", "Snowfield", "STABLE", "7/7"],
            ["Subject_02", "Forest", "DEGRADING", "5/7"],
            ["Subject_03", "Lake", "CORRUPT", "3/7"],
            ["Subject_04", "Starry Sky", "UNKNOWN", "—"],
            ["Subject_05", "Ruins", "STABLE", "6/7"],
            ["Subject_06", "Rain", "CRITICAL", "2/7"],
            ["Subject_07", "2026", "LOST", "1/7"],
        ],
    )
    p.row()
    p.text("Note: Data collected at 2026-01-01 00:00:00", font_size="12px")
    p.row()
    p.button("← Back", target="main")

# ── Dialog ──────────────────────────────────────────────────
with app.panel("panel-dialog") as p:
    p.text("▸ Dialog / Alert")
    p.row()
    p.button("Show Info", action="dialog-open").set_attr("data-target", "dlg-info")
    p.row()
    p.button("Show Warning", action="dialog-open").set_attr("data-target", "dlg-warning")
    p.row()
    p.button("← Back", target="main")
    p.row()
    p.dialog("dlg-info", "Information", "This is a terminal-style dialog box.\nPress OK to close.")
    p.dialog("dlg-warning", "⚠ Warning",
             "System memory is running low.\nConsider restarting the terminal.",
             confirm_label="ACK")

# ── Dialog: shutdown ────────────────────────────────────────
shutdown_panel = app.get_panel("panel-dialog")
if shutdown_panel:
    shutdown_panel.dialog("dlg-shutdown", "⏻ Shutdown",
                          "Are you sure you want to shut down?\n\nThis action cannot be undone.",
                          confirm_label="Yes")

# ── More components ──────────────────────────────────────────
with app.panel("panel-more") as p:
    p.text("▸ Status, Code, Log, Keypad & more")
    p.row()
    p.status_dot("System Online", "green")
    p.status_dot("Warning", "yellow")
    p.status_dot("Critical", "red")
    p.status_dot("Unknown", "white")
    p.row()
    p.separator()
    p.row()
    p.text("Code Block:", font_size="12px")
    p.code_block(
        "def fibonacci(n):\n"
        "    a, b = 0, 1\n"
        "    for _ in range(n):\n"
        "        yield a\n"
        "        a, b = b, a + b",
        max_height="120px",
    )
    p.row()
    p.checkbox("Enable logging", checked=True)
    p.checkbox("Dark mode")
    p.checkbox("Auto-save")
    p.row()
    p.dropdown("Theme: ", ["Terminal", "Matrix", "Paper"])
    p.dropdown("Speed: ", ["Slow", "Normal", "Fast"], default_index=1)
    p.row()
    p.text("Log output:", font_size="12px")
    p.log_viewer(
        lines=[
            "[INFO]  CARNIVAL system v2.4.1",
            "[INFO]  Neural link established",
            "[WARN]  Memory fragment 7C4: corrupted",
            "[INFO]  Attempting recovery...",
            "[ERROR] Checksum mismatch in sector 0x4A",
            "[INFO]  Retry in 3 seconds...",
        ]
    )
    p.row()
    p.text("Keypad (click or arrow-navigate):", font_size="12px")
    p.keypad()
    p.row()
    p.text("Modal example:", font_size="12px")
    p.button("Open Modal", action="modal-open").set_attr("data-target", "demo-modal")
    p.modal("demo-modal", "System Alert",
            "Memory fragmentation detected.<br>Recommended action: defragment.")
    p.row()
    p.button("← Back", target="main")

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "web"
    if mode == "web":
        app.run(port=5051, debug=True, allow_lan=True)
    elif mode == "lan":
        app.run(port=5051, debug=True, open_browser=False, allow_lan=True)
    elif mode == "save":
        path = app.save_html("CTUI_demo.html")
        print(f"Saved to {path}")
    else:
        app.launch(debug=True)
