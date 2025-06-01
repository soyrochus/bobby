# part of Bobby, a GTK4 application for practicing English pronunciation with advanced phrases. | Copyright (c) 2025 | License: MIT

import gi

# Use GTK4
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib, Gdk

from importlib import resources

from .phrases import PHRASES
from .openai_utils import tts_synthesize, stt_transcribe
from .recorder import Recorder

class BobbyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.Bobby")
        self.recorder = Recorder()

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
        practice_btn.connect("clicked", self.on_practice_clicked)
        progress_btn = Gtk.Button(label="Progress")
        settings_nav_btn = Gtk.Button(label="Settings")
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
            mic_button.set_tooltip_text("Play phrase")
            mic_icon = Gtk.Image.new_from_icon_name("media-record-symbolic")
            mic_button.set_child(mic_icon)
            mic_button.connect("clicked", self.on_play_clicked, phrase["text"])
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

    def on_play_clicked(self, button: Gtk.Button, phrase: str):
        print(f"Playing phrase: {phrase}")
        GLib.idle_add(self._play_phrase, phrase)

    def _play_phrase(self, phrase: str):
        try:
            data = tts_synthesize(phrase)
            with open("phrase.mp3", "wb") as f:
                f.write(data)
            # play with sounddevice
            import soundfile as sf
            import sounddevice as sd

            audio, sr = sf.read("phrase.mp3", dtype="float32")
            sd.play(audio, sr)
            sd.wait()
        except Exception as e:
            print("TTS failed", e)
        return False

    def on_practice_clicked(self, button: Gtk.Button):
        print("Recording...")
        GLib.idle_add(self._record_and_transcribe)

    def _record_and_transcribe(self):
        try:
            wav = self.recorder.record(3)
            text = stt_transcribe(wav)
            print("You said:", text)
        except Exception as e:
            print("STT failed", e)
        return False


