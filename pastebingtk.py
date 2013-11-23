# -*- coding: utf-8 -*-


################################################################################

# PastebinGTK
# Version 0.1

# PastebinGTK is a desktop client for pastebin.com.

# Released under the MIT open source license:
license_text = """
Copyright (c) 2013 Adam Chesak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

################################################################################


# Import any needed modules.
# Import Gtk and Gdk for the interface.
from gi.repository import Gtk, Gdk, GdkPixbuf
# Import sys for closing the application.
import sys
# Import os for various things.
import os
# Import platform for getting the user's OS.
import platform

# Import the application's UI data.
from resources.ui import VERSION, TITLE, MENU_DATA

# Tell Python not to create bytecode files, as they mess with the git repo.
# This line can be removed be the user, if desired.
sys.dont_write_bytecode = True

# Get the main directory.
if platform.system().lower() == "windows":
    main_dir = "C:\\.pastebingtk"
else:
    main_dir = "%s/.pastebingtk" % os.path.expanduser("~")

# Check to see if the directory exists, and create it if it doesn't.
if not os.path.exists(main_dir) or not os.path.isdir(main_dir):
    
    # Create the directory.
    os.makedirs(main_dir)


class PastebinGTK(Gtk.Window):
    """Create the application class."""

    def __init__(self):
        """Create the application."""
        
        # Create the window.
        Gtk.Window.__init__(self, title = TITLE)
        # Set the size.
        self.set_default_size(700, 500)
        # Set the icon.
        self.set_icon_from_file("resources/images/icon.png")
        
        # Create the scrolled window for the text box.
        scrolled_window = Gtk.ScrolledWindow()
        
        # It should expand both horizontally and vertically.
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        
        # Create the text box.
        self.text_view = Gtk.TextView()
        self.text_buffer = self.text_view.get_buffer()
        
        # Add the text box to the scrolled window.
        scrolled_window.add(self.text_view)
        
        # Create the action group for the menus.
        action_group = Gtk.ActionGroup("actions")
        
        # Create the Pastebin menu.
        action_group.add_actions([
            ("pastebin_menu", None, "_Pastebin"),
            ("create_paste", Gtk.STOCK_GO_UP, "_Create Paste...", "<Control>n", "Create a new paste", None),
            ("get_paste", Gtk.STOCK_GO_DOWN, "_Get Paste...", "<Control>r", "Get a paste", None),
            ("delete_paste", None, "_Delete Paste", "<Control>d", None, None),
            ("list_trending_pastes", None, "List _Trending Pastes...", "<Control>t", None, None),
            ("list_users_pastes", None, "List _User's Pastes...", "<Control>u", None, None),
            ("get_user_info", None, "Get User's _Info...", "<Control>i", None, None),
            ("save", Gtk.STOCK_SAVE, "_Save to File...", "<Control>s", "Save to file", None),
            ("open", Gtk.STOCK_OPEN, "_Open from File...", "<Control>o", "Open from file", None),
            ("quit", Gtk.STOCK_QUIT, "_Quit", "<Control>q", None, lambda x: self.exit("ignore", "this"))
        ])
        
        # Create the Options menu.
        action_group.add_actions([
            ("options_menu", None, "_Options"),
            ("options", None, "_Options...", "F2", None, None)
        ])
        
        # Create the Help menu.
        action_group.add_actions([
            ("help_menu", None, "_Help"),
            ("about", None, "_About...", "<Shift>F1", None, None),
            ("help", None, "_Help...", "F1", None, None)
        ])
        
        # Create the UI manager.
        ui_manager = Gtk.UIManager()
        ui_manager.add_ui_from_string(MENU_DATA)
        
        # Add the accelerator group to the toplevel window
        accel_group = ui_manager.get_accel_group()
        self.add_accel_group(accel_group)
        ui_manager.insert_action_group(action_group)
        
        # Create the grid for the UI.
        grid = Gtk.Grid()
        
        # Add the menubar to the window.
        menubar = ui_manager.get_widget("/menubar")
        grid.add(menubar)
        
        # Add the toolbar.
        toolbar = ui_manager.get_widget("/toolbar")
        grid.attach_next_to(toolbar, menubar, Gtk.PositionType.BOTTOM, 1, 1)

        # Add the scrolled window to the window.
        grid.attach_next_to(scrolled_window, toolbar, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Add the grid to the main window.
        self.add(grid)
        self.show_all()
    
    
    def exit(self, x, y):
        """Closes the application."""
        
        # Close the application.
        Gtk.main_quit()


if  __name__ == "__main__":
    
    # Create the application.
    win = PastebinGTK()
    win.connect("delete-event", win.exit)
    win.show_all()
    Gtk.main()
