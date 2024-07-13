import pycrossword
import gi
import cairo
from math import pi
from cwgui import Vec2, Color
import csv
import sys

angle = 45
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GLib

# This would typically be its own file

MENU_XML = """

<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <attribute name="label" translatable="yes">Change label</attribute>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target">String 1</attribute>
        <attribute name="label" translatable="yes">String 1</attribute>
      </item>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target">String 2</attribute>
        <attribute name="label" translatable="yes">String 2</attribute>
      </item>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target">String 3</attribute>
        <attribute name="label" translatable="yes">String 3</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">win.maximize</attribute>
        <attribute name="label" translatable="yes">Maximize</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This will be in the windows group and have the "win" prefix
        max_action = Gio.SimpleAction.new_stateful(
            "maximize", None, GLib.Variant.new_boolean(False)
        )

        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)

        # Keep it in sync with the actual state
        self.connect(
            "notify::is-maximized",
            lambda obj, pspec: max_action.set_state(
                GLib.Variant.new_boolean(obj.props.is_maximized)
            ),
        )

        lbl_variant = GLib.Variant.new_string("String 1")
        lbl_action = Gio.SimpleAction.new_stateful(
            "change_label", lbl_variant.get_type(), lbl_variant
        )

        lbl_action.connect("change-state", self.on_change_label_state)
        self.add_action(lbl_action)
        self.label = Gtk.Label(label=lbl_variant.get_string(), margin=30)
        self.add(self.label)
        self.label.show()

    def on_change_label_state(self, action, value):
        action.set_state(value)
        self.label.set_text(value.get_string())

    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.maximize()
        else:
            self.unmaximize()



        # # crossword sizeros
        # with open('cwgui/schemi.csv', 'rU') as p:
        #     # reads csv into a list of lists
        #     self.my_list = [[int(x) for x in rec] for rec in csv.reader(p, delimiter=',')]
        # self.bg_color = Color(251, 241, 199)
        # self.cell_width = 8
        # self.highlightedWord = None
        # self.cursorPos= Vec2()
        # self.pad = 10
        # self.blackPad = 2
        # self.size = Vec2()
        # self.resetCrossword(self.my_list[0])
        # self.da = Gtk.DrawingArea()
        # self.da.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        # self.da.set_property('can-focus', True)
        # # self.da.
        # self.add(self.da)
        # self.da.connect("draw", self.expose)
        # self.da.connect('button-press-event', self.on_drawing_area_button_press)
        # self.da.connect("key-press-event", self.onTreeNavigateKeyPress)
        # # self.button = Gtk.Button(label='Click me')
        # # self.button.connect("clicked", self.on_button_clicked)
        # # self.add(self.button)

    def onTreeNavigateKeyPress(self, treeview, event):
        if self.highlightedWord:
            if (event.keyval >= 65 and event.keyval <=90) or (event.keyval >= 97 and event.keyval <=122):
                self.letters[(self.cursorPos.x, self.cursorPos.y)] = event.string.upper()
                if self.highlightedWord[0][-1] == 'a':
                    # across
                    if 1 + self.cursorPos.x - self.highlightedWord[1] < self.highlightedWord[3]:
                        self.cursorPos.x += 1
                else:
                    if 1 + self.cursorPos.y - self.highlightedWord[2] < self.highlightedWord[3]:
                        self.cursorPos.y += 1
                self.da.queue_draw()

        print(event.keyval)

    def on_drawing_area_button_press(self, widget, event):
        # convert mouse coordinates into grid coordinates
        if event.x <= self.top_left.x or event.x >= self.top_left.x + self.grid_size.x or \
                event.y <= self.top_left.y or event.y >= self.top_left.y + self.grid_size.y:
            return
        gx = int((event.x - self.top_left.x) // self.cell_size)
        gy = int((event.y - self.top_left.y) // self.cell_size)

        if self.highlightedWord:
            print("Mouse clicked... at ", gx, gy, self.highlightedWord[0])
        else:
            print("Mouse clicked... at ", gx, gy, 'NO')

        acrossClue = self.grid.getAcross(gy, gx)
        downClue = self.grid.getDown(gy, gx)
        self.cursorPos = Vec2(gx, gy)
        if acrossClue and downClue:
            if self.highlightedWord and self.highlightedWord[0] == acrossClue.id:
                c = downClue
            else:
                c = acrossClue
        else:
            c = acrossClue if acrossClue else downClue
        if c:
            #print(acrossClue.id, acrossClue.x, acrossClue.y, acrossClue.len)
            self.highlightedWord = (c.id, c.x, c.y, c.len)
            # redraw
            self.da.queue_draw()

        # How to draw a line starting at this point on the drawing area?
        return True

    def resetCrossword(self, data: list):
        self.size = Vec2(data[0], data[1])
        self.blackSquares = data[2:]
        self.letters = dict()
        self.grid = pycrossword.Grid(self.size.x, self.size.y, self.blackSquares)
        d = pycrossword.Dict('dict/ita', 20)
        pycrossword.make(d, self.grid)

        assert (len(self.blackSquares) % 2 == 0)
        self.bs = set()
        self.cellToDef = dict()
        for i in range(0, len(self.blackSquares), 2):
            self.bs.add((self.blackSquares[i], self.blackSquares[i + 1]))
        for x in range(0, self.size.x):
            for y in range(0, self.size.y):
                self.cellToDef[(x,y)] = [-1,-1]

    def isBlack(self, x, y):
        # outside grid
        if x < 0 or y < 0 or x >= self.size.x or y >= self.size.y:
            return True
        return (x, y) in self.bs

    def expose(self, area, context):
        alloc = area.get_allocation()
        width = alloc.width
        height = alloc.height

        self.draw(context, width, height)

    def draw(self, ctx: cairo.Context, width, height):
        """
        This is the draw function, that will be called every time `queue_draw` is
        called on the drawing area. Currently, this is setup to be every frame, 60
        times per second, but you can change that by changing line 95.

        Ported from the first example here, with minimal changes:
        https://www.cairographics.org/samples/
        """
        ctx.set_source_rgb(self.bg_color.r, self.bg_color.g, self.bg_color.b)
        ctx.paint()
        ctx.set_source_rgb(0, 0, 0)

        print(width, height)
        cols = self.size.x
        rows = self.size.y
        w1 = (width - 2 * self.pad) / cols
        w2 = (height - 2 * self.pad) / rows
        cell_size = min(w1, w2)
        grid_width = self.size.x * cell_size
        grid_height = self.size.y * cell_size
        if w2 <= w1:
            tl = Vec2((width - grid_width) // 2, self.pad)
        else:
            tl = Vec2(self.pad, (height - grid_height) // 2)
        ctx.set_line_width(1.0)
        #print(grid_width, tl.x, tl.y)
        if self.highlightedWord:
            ctx.set_source_rgb(0.8,0.8,0.8)
            hw = self.highlightedWord
            if hw[0][-1] == 'a':
                hww = hw[3] * cell_size
                hwh = cell_size
            else:
                hww = cell_size
                hwh = hw[3] * cell_size
            print(hww, hwh)
            ctx.rectangle(tl.x + hw[1] * cell_size,
                          tl.y + hw[2] * cell_size, hww, hwh)
            ctx.fill()
            ctx.set_source_rgb(0.6,0.6,0.6)
            ctx.rectangle(tl.x + self.cursorPos.x * cell_size,
                          tl.y+self.cursorPos.y * cell_size, cell_size, cell_size)
            ctx.fill()
        ctx.set_source_rgb(0, 0, 0)

        # draw columns
        for i in range(0, self.size.x + 1):
            ctx.move_to(tl.x + i * cell_size, tl.y)
            ctx.line_to(tl.x + i * cell_size, tl.y + grid_height)
        # draw rows
        for i in range(0, self.size.y + 1):
            ctx.move_to(tl.x, tl.y + i * cell_size)
            ctx.line_to(tl.x + grid_width, tl.y + i * cell_size)

        # ctx.move_to(tl.x, tl.y)
        # ctx.line_to(tl.x + grid_width, tl.y)
        # ctx.line_to(tl.x + grid_width, tl.y + grid_height)
        # ctx.line_to(tl.x + grid_width, tl.y + grid_height)
        ctx.stroke()

        # plot black squares
            for i in range(0, len(self.blackSquares), 2):
                ctx.rectangle(tl.x + self.blackSquares[i] * cell_size + self.blackPad,
                              tl.y + self.blackSquares[i + 1] * cell_size + self.blackPad,
                              cell_size - 2 * self.blackPad,
                              cell_size - 2 * self.blackPad)
                ctx.fill()


        # place clue numbers
        font_size = cell_size * 0.3
        ctx.set_font_size(font_size)
        ctx.select_font_face(
            "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        inc = 1
        for y in range(0, self.size.y):
            for x in range(0, self.size.x):
                if not self.isBlack(x, y):
                    if (self.isBlack(x - 1, y) and not self.isBlack(x + 1, y)) or (self.isBlack(x, y - 1) and not self.isBlack(x, y + 1)):
                        ctx.move_to(tl.x + x * cell_size + self.blackPad,
                                    tl.y + y * cell_size + font_size)
                        ctx.show_text(str(inc))
                        inc += 1
        # draw letters!
        font_size = cell_size * 0.8
        ctx.set_font_size(font_size)
        for pos, letter in self.letters.items():
            ctx.move_to(tl.x + pos[0] * cell_size,
                        tl.y + pos[1] * cell_size + font_size)
            ctx.show_text(str(letter))

        ctx.stroke()
        self.top_left = tl
        self.grid_size = Vec2(grid_width, grid_height)
        self.cell_size = cell_size
        # ctx.stroke()

    def open_file(self, mi):
        print('ioe')


class CruciApp(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="org.example.myapp",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs
        )

        self.window = None
        self.add_main_option(
            "test",
            ord("t"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Command line test",
            None,
        )

    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)
        #builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        builder = Gtk.Builder.new_from_file('menu.xml')
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = AppWindow(application=self, title="Main Window")

        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()
        if "test" in options:
            print("Test argument recieved: %s" % options["test"])
        self.activate()
        return 0


    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()


if __name__ == "__main__":
    app = CruciApp()
    app.run(sys.argv)
#win = MainWindow()
#win.connect("destroy", Gtk.main_quit)
#win.show_all()
#Gtk.main()
