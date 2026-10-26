"""Always-on-top battery pill for the Touch Display 2 (GTK3, frameless).

Shows X1201 percentage + charge state in the top-right corner of the main
screen; drag to move, right-click to quit. Autostarts via
~/.config/autostart/fielddeck-battery.desktop (installed by install.sh).
"""
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

from .battery import Gauge

REFRESH_S = 10


class Pill(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_accept_focus(False)
        self.set_app_paintable(True)
        self.label = Gtk.Label()
        self.label.set_margin_start(10); self.label.set_margin_end(10)
        self.label.set_margin_top(3); self.label.set_margin_bottom(3)
        self.add(self.label)
        try:
            self.gauge = Gauge()
        except Exception:
            self.gauge = None
        self.connect("button-press-event", self._click)
        self._style("#444")
        self.refresh()
        GLib.timeout_add_seconds(REFRESH_S, self.refresh)
        self.show_all()
        GLib.idle_add(self._park_top_right)

    def _park_top_right(self):
        screen = self.get_screen()
        mon = screen.get_display().get_primary_monitor() or \
              screen.get_display().get_monitor(0)
        geo = mon.get_geometry()
        w, _ = self.get_size()
        self.move(geo.x + geo.width - w - 8, geo.y + 4)
        return False

    def _style(self, color):
        css = Gtk.CssProvider()
        css.load_from_data(
            f"window {{ background: rgba(20,20,24,0.82); border-radius: 12px; }}"
            f"label {{ color: {color}; font: 600 13px 'DejaVu Sans'; }}".encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _click(self, _w, ev):
        if ev.button == 3:
            Gtk.main_quit()
        elif ev.button == 1:
            self.begin_move_drag(ev.button, int(ev.x_root), int(ev.y_root), ev.time)

    def refresh(self):
        if not self.gauge:
            self.label.set_text("bat ?")
            return True
        try:
            s = self.gauge.read()
        except OSError:
            self.label.set_text("bat !")
            return True
        arrow = {True: "↑", False: "", None: ""}[s["charging"]]
        self.label.set_text(f"■ {s['percent']:.0f}%{arrow}")
        pct = s["percent"]
        self._style("#57d97a" if (s["charging"] or pct > 40) else
                    "#e6c04a" if pct > 15 else "#e65b4a")
        return True


def main():
    Pill()
    Gtk.main()


if __name__ == "__main__":
    main()
