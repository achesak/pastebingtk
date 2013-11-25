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
# Import webbrowser for opening webpages.
import webbrowser

# Import the application's UI data.
from resources.ui import VERSION, TITLE, MENU_DATA
# Import the dictionaries for the constants and formats.
from resources.dicts import FORMATS, EXPIRE, EXPOSURE
# Import the login dialog.
from resources.dialogs.login_dialog import LoginDialog
# Import the create paste dialog.
from resources.dialogs.create_dialog import CreatePasteDialog
# Import the miscellaneous dialogs.
from resources.dialogs.misc_dialogs import show_alert_dialog, show_error_dialog, show_question_dialog
# Import the pastebin API wrapper.
from resources.pastebin_python.pastebin import PastebinPython
# Import the API exceptions.
from resources.pastebin_python.pastebin_exceptions import PastebinBadRequestException, PastebinFileException, PastebinHTTPErrorException, PastebinNoPastesException
# Import the API options.
from resources.pastebin_python.pastebin_options import OPTION_DELETE, OPTION_LIST, OPTION_PASTE, OPTION_TRENDS, OPTION_USER_DETAILS

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
        
        # Variables for remembering user data.
        self.user_name = ""
        self.user_key = ""
        self.dev_key = "d2314ff616133e54f728918b8af1500e"
        self.login = False
        
        # Initalize the PastebinPython object.
        self.api = PastebinPython(api_dev_key = self.dev_key)
        
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
            ("create_paste", Gtk.STOCK_GO_UP, "_Create Paste...", "<Control>n", "Create a new paste", self.create_paste),
            ("get_paste", Gtk.STOCK_GO_DOWN, "_Get Paste...", "<Control>r", "Get a paste", None),
            ("delete_paste", None, "_Delete Paste", "<Control>d", None, None),
            ("list_trending_pastes", None, "List _Trending Pastes...", "<Control>t", None, None),
            ("list_users_pastes", None, "List _User's Pastes...", "<Control>u", None, None),
            ("login", None, "_Login...", "<Control>l", None, self.pastebin_login),
            ("logout", None, "Logo_ut", "<Shift><Control>1", None, self.pastebin_logout),
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
            ("about", None, "_About...", "<Shift>F1", None, self.show_about),
            ("help", None, "_Help...", "F1", None, self.show_help)
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
        
        # Get the user login details.
        self.pastebin_login("ignore")
    
    
    def create_paste(self, event):
        """Creates a new paste."""
        
        # Get the text.
        text = self.text_buffer.get_text(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter(), False)
        
        # If there's no text, don't create the paste.
        if not text:
            show_error_dialog(self, "Create Paste", "No text entered.")
            return
        
        # Show the dialog.
        new_dlg = CreatePasteDialog(self)
        response = new_dlg.run()
        
        # If the user clicked OK:
        if response == Gtk.ResponseType.OK:
            
            # Get the fields.
            name = new_dlg.name_ent.get_text()
            format_ = new_dlg.form_com.get_active_text()
            expire = new_dlg.expi_com.get_active_text()
            exposure = new_dlg.expo_com.get_active_text()
            
            # Get the values as needed.
            format_ = FORMATS[format_]
            expire = EXPIRE[expire]
            exposure = EXPOSURE[exposure]
            
            # Send the paste.
            url = self.api.createPaste(api_paste_code = text, api_paste_name = name, api_paste_format = format_, api_paste_private = exposure, api_paste_expire_date = expire)
            
            # Show the url.
            show_alert_dialog(self, "Create Paste", "Paste has been successfully created, and can be found at the following URL:\n\n%s" % url)
        
        # Close the dialog.
        new_dlg.destroy()
    
    
    def pastebin_login(self, event):
        """Logs the user in."""
        
        # Show the dialog.
        login_dlg = LoginDialog(self)
        response = login_dlg.run()
        
        # If the user clicked OK:
        if response == Gtk.ResponseType.OK:
            user_name = login_dlg.name_ent.get_text()
            password = login_dlg.pass_ent.get_text()
            
            # If the username and password are valid, get the user key
            if user_name != "" and password != "":
                
                try:
                    self.user_key = self.api.createAPIUserKey(user_name, password)
                    self.user_name = user_name
                    self.login = True
                    
                    show_alert_dialog(self, "Login", "Successfully logged in as %s." % user_name)
                
                except PastebinBadRequestException:
                    
                    show_error_dialog(self, "Login", "Invalid username or password specified.\n\nNot logged in.")
                    self.login = False
            
            else:
                
                show_error_dialog(self, "Login", "No %s entered.\n\nNot logged in." % "username" if user_name == "" else "password")
                self.login = False
        
        else:
            
            show_alert_dialog(self, "Login", "No username or password specified.\n\nNot logged in.")
            self.login = False
            
        # Close the dialog.
        login_dlg.destroy()
    
    
    def pastebin_logout(self, event):
        """Logs the user out."""
        
        self.login = False
        show_alert_dialog(self, "Logout", "You are now logged out.")
    
    
    def show_about(self, event):
        """Shows the About dialog."""
        
        # Load the icon.
        img_file = open("resources/images/icon.png", "rb")
        img_bin = img_file.read()
        img_file.close()
        
        # Get the PixBuf.
        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        loader.write(img_bin)
        loader.close()
        pixbuf = loader.get_pixbuf()
        
        # Create the dialog.
        about_dlg = Gtk.AboutDialog()
        
        # Set the title.
        about_dlg.set_title("About " + TITLE)
        # Set the program name.
        about_dlg.set_program_name(TITLE)
        # Set the program icon.
        about_dlg.set_logo(pixbuf)
        # Set the program version.
        about_dlg.set_version(VERSION)
        # Set the comments.
        about_dlg.set_comments("PastebinGTK is a desktop client for pastebin.com.")
        # Set the copyright notice.
        about_dlg.set_copyright("Copyright (c) 2013 Adam Chesak")
        # Set the authors.
        about_dlg.set_authors(["Adam Chesak <achesak@yahoo.com>"])
        # Set the license.
        about_dlg.set_license(license_text)
        # Set the website.
        about_dlg.set_website("http://poultryandprogramming.wordpress.com/")
        about_dlg.set_website_label("http://poultryandprogramming.wordpress.com/")
        
        # Show the dialog.
        about_dlg.show_all()
    
    
    def show_help(self, event):
        """Shows the help in a web browser."""
        
        # Open the help file.
        webbrowser.open_new("resources/help/help.html")  
    
    
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
