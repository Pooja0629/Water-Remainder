import os

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.spinner import Spinner
from kivy.utils import get_color_from_hex

try:
    from plyer import notification
except ImportError:
    notification = None


APP_DIR = os.path.dirname(os.path.abspath(__file__))
GIF_PATH = os.path.join(APP_DIR, "character.gif")

INTERVALS = {
    "Every 10 Seconds (Testing)": 10,
    "Every 30 Minutes": 30 * 60,
    "Every 1 Hour": 60 * 60,
}
SNOOZE_SECONDS = 10 * 60

BG_COLOR = get_color_from_hex("#1e1e24")
BLUE = get_color_from_hex("#0078d4")
WHITE = (1, 1, 1, 1)
DARK_TEXT = (0.07, 0.07, 0.07, 1)
BUBBLE_BORDER = get_color_from_hex("#202020")


def add_rounded_bg(widget, color, radius=dp(8)):
    """Draw a rounded background behind a widget."""
    with widget.canvas.before:
        Color(*color)
        rect = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[radius])

    def update(*_):
        rect.pos = widget.pos
        rect.size = widget.size

    widget.bind(pos=update, size=update)


class AquaPalApp(App):

    def build(self):
        self.title = "AquaPal - Cat Noir Hydration"
        Window.clearcolor = BG_COLOR

        self.reminder_event = None
        self.toast = None
        self.toast_answered = False

        root = BoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(15),
        )

        title = Label(
            text="Remind me to drink water",
            color=WHITE,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(40),
        )
        root.add_widget(title)

        self.spinner = Spinner(
            text="Every 30 Minutes",
            values=list(INTERVALS.keys()),
            size_hint=(None, None),
            size=(dp(260), dp(44)),
            pos_hint={"center_x": 0.5},
        )
        root.add_widget(self.spinner)

        start_btn = Button(
            text="Start Reminder",
            color=WHITE,
            bold=True,
            background_normal="",
            background_color=(0, 0, 0, 0),
            size_hint=(None, None),
            size=(dp(220), dp(48)),
            pos_hint={"center_x": 0.5},
        )
        add_rounded_bg(start_btn, BLUE)
        start_btn.bind(on_release=self.on_start_pressed)
        root.add_widget(start_btn)

        self.status = Label(
            text="Pick an interval and tap Start.",
            color=WHITE,
            font_size=dp(14),
        )
        root.add_widget(self.status)

        return root

    # ---------- Timer logic ----------

    def current_interval(self):
        return INTERVALS[self.spinner.text]

    def on_start_pressed(self, *_):
        self.start_timer(self.current_interval())
        self.status.text = f"Reminder set: {self.spinner.text.lower()}"

    def start_timer(self, seconds):
        self.cancel_timer()
        self.reminder_event = Clock.schedule_once(self.show_notification, seconds)

    def cancel_timer(self):
        if self.reminder_event is not None:
            self.reminder_event.cancel()
            self.reminder_event = None

    def show_notification(self, *_):
        self.reminder_event = None
        self.send_system_notification()
        self.open_toast()

    def send_system_notification(self):
        if notification is None:
            return
        try:
            notification.notify(
                title="AquaPal",
                message="Hey! Drink some water!",
                app_name="AquaPal",
                timeout=10,
            )
        except Exception:
            pass  # Notifications are a bonus; never crash the app over them

    # ---------- Reminder popup ----------

    def open_toast(self):
        self.toast_answered = False

        toast = ModalView(
            size_hint=(0.85, None),
            height=dp(440),
            background_color=(0, 0, 0, 0.6),
        )

        box = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(12),
        )

        # Speech bubble
        bubble = Label(
            text="Hey! Drink some water!",
            color=DARK_TEXT,
            bold=True,
            font_size=dp(16),
            size_hint=(None, None),
            size=(dp(260), dp(44)),
            pos_hint={"center_x": 0.5},
        )
        add_rounded_bg(bubble, WHITE, radius=dp(12))
        box.add_widget(bubble)

        # Animated Cat Noir GIF (Kivy plays GIFs automatically)
        cat = Image(
            source=GIF_PATH,
            anim_delay=0.08,
            allow_stretch=True,
            keep_ratio=True,
        )
        box.add_widget(cat)

        # Buttons
        row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))

        drank_btn = Button(
            text="Drank It",
            color=WHITE,
            bold=True,
            background_normal="",
            background_color=(0, 0, 0, 0),
        )
        add_rounded_bg(drank_btn, BLUE)
        drank_btn.bind(on_release=self.on_drank)

        snooze_btn = Button(
            text="Snooze",
            color=DARK_TEXT,
            bold=True,
            background_normal="",
            background_color=(0, 0, 0, 0),
        )
        add_rounded_bg(snooze_btn, WHITE)
        snooze_btn.bind(on_release=self.on_snooze)

        row.add_widget(drank_btn)
        row.add_widget(snooze_btn)
        box.add_widget(row)

        toast.add_widget(box)
        toast.bind(on_dismiss=self.on_toast_dismissed)

        self.toast = toast
        toast.open()

    def on_drank(self, *_):
        self.toast_answered = True
        self.toast.dismiss()
        self.start_timer(self.current_interval())
        self.status.text = "Great job! Next reminder scheduled."

    def on_snooze(self, *_):
        self.toast_answered = True
        self.toast.dismiss()
        self.start_timer(SNOOZE_SECONDS)
        self.status.text = "Snoozed for 10 minutes."

    def on_toast_dismissed(self, *_):
        # If the user closed the popup without a button (back key, tap outside),
        # keep the reminders going instead of stopping them.
        if not self.toast_answered:
            self.start_timer(self.current_interval())
        self.toast = None

    # ---------- Keep running in background ----------

    def on_pause(self):
        # Tells Android the app may stay alive when minimized
        return True


if __name__ == "__main__":
    AquaPalApp().run()