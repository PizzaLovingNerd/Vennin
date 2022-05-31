# import modules
from matplotlib_venn import venn2
import matplotlib.pyplot as plt

from matplotlib.backends.backend_gtk4 import (
    NavigationToolbar2GTK4 as NavigationToolbar)
from matplotlib.backends.backend_gtk4cairo import (
    FigureCanvasGTK4Cairo as FigureCanvas)


import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', "1")
from gi.repository import Gtk, Adw


def adjustment(start):
    return Gtk.Adjustment.new(
        start, 0, 10000, 1,
        0, 0
    )

class Application(Adw.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="com.pizzalovingnerd.Vennin"
        )
        self.window = None
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.window = Window(application=app)
        self.window.present()


class Header(Gtk.HeaderBar):
    def __init__(self, window):
        super().__init__()
        generateBtn = Gtk.Button(label="Generate")
        generateBtn.connect(
            "clicked", window.generate
        )
        generateBtn.get_style_context().add_class('suggested-action')

        self.pack_start(generateBtn)


class Window(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        # print(one, two)
        super().__init__(*args, **kwargs)
        self.set_title("Vennin")

        header = Header(self)
        self.set_titlebar(header)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.diagramscroll = Gtk.ScrolledWindow()

        self.sidebar = Sidebar()
        box.append(self.sidebar)
        box.append(self.diagramscroll)

        self.set_child(box)
        self.generate(None)

    def generate(self, button):
        subset = (
            self.sidebar.AData_input.get_value_as_int(),
            self.sidebar.BData_input.get_value_as_int(),
            self.sidebar.BothData_input.get_value_as_int()
        )

        nameA = self.sidebar.AName_input.get_text()
        nameB = self.sidebar.BName_input.get_text()
        if nameA == "":
            nameA = "Group A"
        if nameB == "":
            nameB = "Group B"

        fig, ax = plt.subplots()
        venn2(subsets=subset, set_labels=(nameA, nameB), ax=ax)

        if self.sidebar.NotData_input.get_value_as_int() != 0:
            plt.text(
                ax.get_xbound()[0],
                ax.get_ybound()[0] - 0.1,
                f"Not:{self.sidebar.NotData_input.get_text()}",
                fontsize="large"
            )

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        canvas = FigureCanvas(fig)
        canvas.set_vexpand(True)
        toolbar = NavigationToolbar(canvas, self)
        toolbar.set_name("NavToolbar")
        box.append(canvas)
        box.append(toolbar)

        self.diagramscroll.set_child(box)

class SidebarLabel(Gtk.Label):
    def __init__(self, name):
        super().__init__(xalign=0)
        self.set_markup(f"<b>{name}:</b>")
        self.set_margin_top(10)

class Sidebar(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_spacing(10)

        ALabel = SidebarLabel("Group A")
        self.AName_input = Gtk.Entry(placeholder_text="Group Name")
        self.AData_input = Gtk.SpinButton.new(adjustment(10), 1, 0)

        BLabel = SidebarLabel("Group B")
        BLabel.set_markup(f"<b>Group B:</b>")
        self.BName_input = Gtk.Entry(placeholder_text="Group Name")
        self.BData_input = Gtk.SpinButton.new(adjustment(10), 1, 0)

        BothLabel = SidebarLabel("Both Groups")
        self.BothData_input = Gtk.SpinButton.new(adjustment(2), 1, 0)

        NotLabel = SidebarLabel("Neither Group")
        self.NotData_input = Gtk.SpinButton.new(adjustment(0), 1, 0)

        self.append(ALabel)
        self.append(self.AName_input)
        self.append(self.AData_input)
        self.append(BLabel)
        self.append(self.BName_input)
        self.append(self.BData_input)
        self.append(BothLabel)
        self.append(self.BothData_input)
        self.append(NotLabel)
        self.append(self.NotData_input)


if __name__ == "__main__":
    app = Application()
    app.run()
