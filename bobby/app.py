# part of Bobby, a GTK4 application for practicing English pronunciation with advanced phrases. | Copyright (c) 2025 | License: MIT

import gi

# Use GTK4
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib, Gdk
import time
import numpy as np
import sounddevice as sd

from importlib import resources

from .phrases import PHRASES
from .openai_utils import tts_synthesize, stt_transcribe
import threading
from .recorder import Recorder

class BobbyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.Bobby")
        self.play_device = None
        self.record_device = None
        self.recorder = Recorder(device=self.record_device)
        self.running = False

    def load_css(self):
        provider = Gtk.CssProvider()
        with resources.files(__package__).joinpath("style.css").open("rb") as f:
            provider.load_from_data(f.read())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),  # GTK4: Use Gdk.Display
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = Gtk.ApplicationWindow(application=self)
            win.set_title("Pronunciation Practice")
            win.set_default_size(400, 600)
            self.load_css()
            self.build_ui(win)
        win.present()

    def build_ui(self, win: Gtk.ApplicationWindow):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        win.set_child(vbox)

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        title = Gtk.Label(label="Pronunciation Practice")
        title.get_style_context().add_class("title-1")
        header.append(title)
        settings_button = Gtk.Button()
        settings_icon = Gtk.Image.new_from_icon_name("emblem-system-symbolic")
        settings_button.set_child(settings_icon)
        settings_button.connect("clicked", self.on_open_settings)
        header.append(settings_button)
        vbox.append(header)

        search = Gtk.SearchEntry()
        search.set_placeholder_text("Search phrases")
        vbox.append(search)

        filter_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.filter_buttons = []
        for cat in ["All", "Business", "Academic", "Social"]:
            btn = Gtk.ToggleButton(label=cat)
            if cat == "All":
                btn.set_active(True)
            btn.connect("toggled", self.on_filter_toggled, cat)
            filter_box.append(btn)
            self.filter_buttons.append(btn)
        vbox.append(filter_box)

        section_label = Gtk.Label(label="Advanced Phrases")
        section_label.get_style_context().add_class("heading-2")
        section_label.set_halign(Gtk.Align.START)
        vbox.append(section_label)

        self.listbox = Gtk.ListBox()
        vbox.append(self.listbox)

        self.populate_list("All")

        nav = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        practice_btn = Gtk.Button(label="Practice")
        practice_btn.connect("clicked", self.on_nav_practice_clicked)
        progress_btn = Gtk.Button(label="Progress")
        settings_nav_btn = Gtk.Button(label="Settings")
        settings_nav_btn.connect("clicked", self.on_open_settings)
        nav.append(practice_btn)
        nav.append(progress_btn)
        nav.append(settings_nav_btn)
        vbox.append(nav)

    def populate_list(self, category: str):
        # GTK4: Remove all rows using get_first_child/get_next_sibling
        row = self.listbox.get_first_child()
        while row is not None:
            next_row = row.get_next_sibling()
            self.listbox.remove(row)
            row = next_row
        for phrase in PHRASES:
            if category != "All" and phrase["category"] != category:
                continue
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            mic_button = Gtk.Button()
            mic_button.set_tooltip_text("Practice phrase")
            mic_icon = Gtk.Image.new_from_icon_name("microphone-sensitivity-high-symbolic")
            mic_button.set_child(mic_icon)
            feedback_label = Gtk.Label()
            feedback_label.set_xalign(0)
            level = Gtk.LevelBar()
            level.add_css_class("sound-bar")
            level.set_min_value(0.0)
            level.set_max_value(1.0)
            level.set_value(0.0)
            mic_button.connect(
                "clicked", self.on_play_clicked, phrase["text"], feedback_label, mic_button, level
            )
            hbox.append(mic_button)

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
            phrase_label = Gtk.Label(label=phrase["text"])
            phrase_label.set_xalign(0)
            phrase_label.get_style_context().add_class("bold")
            cat_label = Gtk.Label(label=phrase["category"])
            cat_label.set_xalign(0)
            cat_label.get_style_context().add_class("dim-label")
            vbox.append(phrase_label)
            vbox.append(cat_label)
            vbox.append(feedback_label)
            vbox.append(level)

            hbox.append(vbox)
            row.set_child(hbox)
            self.listbox.append(row)

    def on_filter_toggled(self, button: Gtk.ToggleButton, category: str):
        if not button.get_active():
            return
        for btn in self.filter_buttons:
            if btn is not button:
                btn.set_active(False)
        self.populate_list(category)

    def on_play_clicked(self, button: Gtk.Button, phrase: str, label: Gtk.Label, mic_button: Gtk.Button, level: Gtk.LevelBar):
        if self.running:
            return
        self.running = True
        ctx = mic_button.get_style_context()
        ctx.remove_class("result-good")
        ctx.remove_class("result-bad")
        threading.Thread(
            target=self._practice_flow,
            args=(phrase, label, mic_button, level),
            daemon=True,
        ).start()

    def _practice_flow(self, phrase: str, label: Gtk.Label, button: Gtk.Button, level: Gtk.LevelBar):
        ctx = button.get_style_context()
        level_ctx = level.get_style_context()
        GLib.idle_add(label.set_text, "Connecting to OpenAI...")
        GLib.idle_add(level.set_value, 0.0)
        GLib.idle_add(button.set_child, Gtk.Image.new_from_icon_name("audio-volume-high-symbolic"))
        GLib.idle_add(ctx.add_class, "playing")
        GLib.idle_add(level_ctx.add_class, "playing")
        try:
            data = tts_synthesize(phrase)
            with open("phrase.mp3", "wb") as f:
                f.write(data)
            import soundfile as sf
            import sounddevice as sd

            audio, sr = sf.read("phrase.mp3", dtype="float32")
            block = int(0.1 * sr)
            idx = 0
            def update_play():
                nonlocal idx
                if idx >= len(audio):
                    return False
                amp = float(np.abs(audio[idx:idx+block]).mean())
                GLib.idle_add(level.set_value, min(amp * 10, 1.0))
                idx += block
                return True

            GLib.idle_add(label.set_text, "Playing...")
            timeout_id = GLib.timeout_add(100, update_play)
            sd.play(audio, sr, device=self.play_device)
            sd.wait()
            GLib.source_remove(timeout_id)
        except Exception as e:
            GLib.idle_add(label.set_text, f"TTS failed: {e}")
            GLib.idle_add(ctx.remove_class, "playing")
            GLib.idle_add(button.set_child, Gtk.Image.new_from_icon_name("microphone-sensitivity-high-symbolic"))
            self.running = False
            return
        GLib.idle_add(ctx.remove_class, "playing")
        GLib.idle_add(level_ctx.remove_class, "playing")
        GLib.idle_add(level.set_value, 0.0)

        GLib.idle_add(label.set_text, "Recording...")
        GLib.idle_add(ctx.add_class, "recording")
        GLib.idle_add(level_ctx.add_class, "recording")
        GLib.idle_add(button.set_child, Gtk.Image.new_from_icon_name("media-record-symbolic"))
        try:
            max_duration = len(audio) / sr + 10
            def rec_activity(vol: float):
                GLib.idle_add(level.set_value, vol)
            wav = self.recorder.record(max_duration, activity_cb=rec_activity)
        except Exception as e:
            GLib.idle_add(label.set_text, f"Record failed: {e}")
            GLib.idle_add(ctx.remove_class, "recording")
            GLib.idle_add(level_ctx.remove_class, "recording")
            GLib.idle_add(button.set_child, Gtk.Image.new_from_icon_name("microphone-sensitivity-high-symbolic"))
            self.running = False
            return
        GLib.idle_add(ctx.remove_class, "recording")
        GLib.idle_add(level_ctx.remove_class, "recording")
        GLib.idle_add(level.set_value, 0.0)
        GLib.idle_add(button.set_child, Gtk.Image.new_from_icon_name("microphone-sensitivity-high-symbolic"))

        GLib.idle_add(label.set_text, "Sending to OpenAI...")
        GLib.idle_add(ctx.add_class, "analyzing")
        try:
            text = stt_transcribe(wav)
        except Exception as e:
            GLib.idle_add(label.set_text, f"STT failed: {e}")
            GLib.idle_add(ctx.remove_class, "analyzing")
            self.running = False
            return
        GLib.idle_add(ctx.remove_class, "analyzing")

        feedback = self._compare_phrase(phrase, text)
        GLib.idle_add(label.set_text, feedback)
        if "Great job" in feedback:
            GLib.idle_add(ctx.add_class, "result-good")
        else:
            GLib.idle_add(ctx.add_class, "result-bad")
        self.running = False

    def _compare_phrase(self, expected: str, actual: str) -> str:
        exp = expected.lower().split()
        act = actual.lower().split()
        missing = [w for w in exp if w not in act]
        extra = [w for w in act if w not in exp]
        if not missing and not extra:
            return f"You said: {actual}\nGreat job!"
        parts = [f"You said: {actual}"]
        if missing:
            parts.append("Missed: " + ", ".join(missing))
        if extra:
            parts.append("Extra: " + ", ".join(extra))
        return "\n".join(parts)

    def on_nav_practice_clicked(self, button: Gtk.Button):
        dialog = Gtk.MessageDialog(
            transient_for=self.props.active_window,
            modal=True,
            buttons=Gtk.ButtonsType.OK,
            text="Select a phrase's microphone to practice."
        )
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.show()

    def on_open_settings(self, button: Gtk.Button):
        devices = sd.query_devices()
        out_ids = [i for i, d in enumerate(devices) if d['max_output_channels'] > 0]
        in_ids = [i for i, d in enumerate(devices) if d['max_input_channels'] > 0]

        win = Gtk.Window(title="Sound Settings", transient_for=self.props.active_window, modal=True)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
        win.set_child(box)

        out_combo = Gtk.ComboBoxText()
        for i in out_ids:
            out_combo.append_text(devices[i]['name'])
        current_out = self.play_device if self.play_device is not None else sd.default.device[1]
        if current_out in out_ids:
            out_combo.set_active(out_ids.index(current_out))

        in_combo = Gtk.ComboBoxText()
        for i in in_ids:
            in_combo.append_text(devices[i]['name'])
        current_in = self.record_device if self.record_device is not None else sd.default.device[0]
        if current_in in in_ids:
            in_combo.set_active(in_ids.index(current_in))

        box.append(Gtk.Label(label="Playback Device", xalign=0))
        box.append(out_combo)
        box.append(Gtk.Label(label="Recording Device", xalign=0))
        box.append(in_combo)

        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        cancel_btn = Gtk.Button(label="Cancel")
        save_btn = Gtk.Button(label="Save")
        action_box.append(cancel_btn)
        action_box.append(save_btn)
        box.append(action_box)

        def on_cancel(btn):
            win.destroy()

        def on_save(btn):
            self.play_device = out_ids[out_combo.get_active()]
            self.record_device = in_ids[in_combo.get_active()]
            self.recorder.device = self.record_device
            win.destroy()

        cancel_btn.connect("clicked", on_cancel)
        save_btn.connect("clicked", on_save)

        win.show()


