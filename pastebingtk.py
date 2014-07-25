# -*- coding: utf-8 -*-


################################################################################

# PastebinGTK
# Version 0.3

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
# Import GtkSource for the sourceview widget.
from gi.repository import GtkSource
# Import sys for closing the application and getting command line arguments.
import sys
# Import os for various things.
import os
# Import platform for getting the user's OS.
import platform
# Import webbrowser for opening webpages.
import webbrowser
# Import urllib2 for working with urls.
import urllib2
# Import time for working with time.
import time
# Import json for loading and saving the configuration file.
import json
# Import webbrowser for opening websites in the user's browser.
import webbrowser

# Tell Python not to create bytecode files, as they mess with the git repo.
# This line can be removed be the user, if desired.
sys.dont_write_bytecode = True

# Import the application's UI data.
from resources.ui import VERSION, TITLE, MENU_DATA
# Import the dictionaries for the constants and formats.
from resources.dicts import FORMATS, EXPIRE, EXPOSURE
# Import the login dialog.
from resources.dialogs.login_dialog import LoginDialog
# Import the create paste dialog.
from resources.dialogs.create_dialog import CreatePasteDialog
# Import the get paste dialog.
from resources.dialogs.get_dialog import GetPasteDialog
# Import the delete paste dialog.
from resources.dialogs.delete_dialog import DeletePasteDialog
# Import the paste list dialog.
from resources.dialogs.list_user_dialog import ListPastesDialog
# Import the user details dialog.
from resources.dialogs.user_details_dialog import UserDetailsDialog
# Import the options dialog.
from resources.dialogs.options_dialog import OptionsDialog
# Import the miscellaneous dialogs.
from resources.dialogs.misc_dialogs import show_alert_dialog, show_error_dialog, show_question_dialog
# Import the pastebin API wrapper.
from resources.pastebin_python.pastebin import PastebinPython
# Import the API exceptions.
from resources.pastebin_python.pastebin_exceptions import PastebinBadRequestException, PastebinFileException, PastebinHTTPErrorException, PastebinNoPastesException
# Import the API options.
from resources.pastebin_python.pastebin_options import OPTION_DELETE, OPTION_LIST, OPTION_PASTE, OPTION_TRENDS, OPTION_USER_DETAILS
# Import the functions for working with command line arguments.
import resources.command_line as command_line

# Get the main directory.
if platform.system().lower() == "windows":
    main_dir = "C:\\.pastebingtk"
else:
    main_dir = "%s/.pastebingtk" % os.path.expanduser("~")

# Check to see if the directory exists, and create it if it doesn't.
if not os.path.exists(main_dir) or not os.path.isdir(main_dir):
    
    # Create the directory.
    os.makedirs(main_dir)

# Get the configuration.
try:
    # Load the configuration file.
    config_file = open("%s/config" % main_dir, "r")
    config = json.load(config_file)
    config_file.close()

except (IOError, ValueError):
    # Continue.
    config = {"dev_key": "d2314ff616133e54f728918b8af1500e",
              "prompt_login": True,
              "remember_username": True,
              "restore_window": True,
              "confirm_exit": False,
              "default_name": "",
              "default_format": "None",
              "default_expiration": "Never",
              "default_exposure": "Public",
              "line_numbers": True,
              "syntax_highlight": True,
              "syntax_guess": True,
              "syntax_default": ""}

# Update the configuration, if necessary.
if not "line_numbers" in config:
    config["line_numbers"] = True
if not "syntax_highlight" in config:
    config["syntax_highlight"] = True
if not "syntax_guess" in config:
    config["syntax_guess"] = True
if not "syntax_default" in config:
    config["syntax_default"] = ""

# Load the last username, if the user wants that.
if config["remember_username"]:
    
    try:
        # Load the username.
        user_file = open("%s/username" % main_dir, "r")
        username = user_file.read()
        user_file.close()
    
    except IOError:
        # Continue.
        username = ""

# Get the previous window size.
try:
    # Load the window size file.
    wins_file = open("%s/window_size" % main_dir, "r")
    last_width = int(wins_file.readline())
    last_height = int(wins_file.readline())
    wins_file.close()

except IOError:
    # Continue.
    last_width = 700
    last_height = 500

# If the user doesn't want to restore the window size, set the size to the default.
if not config["restore_window"]:
    last_width = 700
    last_height = 500


class PastebinGTK(Gtk.Window):
    """Create the application class."""

    def __init__(self):
        """Create the application."""
        
        # Variables for remembering user data.
        self.user_name = ""
        if config["remember_username"]:
            self.user_name = username
        self.user_key = ""
        self.dev_key = config["dev_key"]
        self.login = False
        
        # Initalize the PastebinPython object.
        self.api = PastebinPython(api_dev_key = self.dev_key)
        
        # Create the window.
        Gtk.Window.__init__(self, title = TITLE)
        # Set the size.
        self.set_default_size(last_width, last_height)
        # Set the icon.
        self.set_icon_from_file("resources/images/icon.png")
        
        # Create the scrolled window for the text box.
        scrolled_window = Gtk.ScrolledWindow()
        
        # It should expand both horizontally and vertically.
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        
        # Create the sourceview.
        self.text_view = GtkSource.View.new()
        self.language_manager = GtkSource.LanguageManager.new()
        self.text_buffer = self.text_view.get_buffer()
        
        # Show line numbers, if the user wants that.
        if config["line_numbers"]:
            self.text_view.set_show_line_numbers(True)
        
        # Add the text box to the scrolled window.
        scrolled_window.add(self.text_view)
        
        # Create the action group for the menus.
        action_group = Gtk.ActionGroup("actions")
        
        # Create the Pastebin menu.
        action_group.add_actions([
            ("pastebin_menu", None, "_Pastebin"),
            ("create_paste", Gtk.STOCK_GO_UP, "_Create Paste...", "<Control>n", "Create a new paste", self.create_paste),
            ("get_paste", Gtk.STOCK_GO_DOWN, "_Get Paste...", "<Control>r", "Get a paste", self.get_paste),
            ("delete_paste", Gtk.STOCK_DELETE, "_Delete Paste...", "<Control>d", "Delete a paste", self.delete_paste),
            ("list_trending_pastes", None, "List _Trending Pastes...", "<Control>t", None, self.list_trending_pastes),
            ("list_users_pastes", None, "List _User's Pastes...", "<Control>u", None, self.list_users_pastes),
            ("login", None, "_Login...", "<Control>l", None, self.pastebin_login),
            ("logout", None, "Logo_ut...", "<Shift><Control>l", None, self.pastebin_logout),
            ("user_details", None, "G_et User's Details...", None, None, self.get_user_details),
            ("quit", Gtk.STOCK_QUIT, "_Quit", "<Control>q", None, lambda x: self.exit("ignore", "this"))
        ])
        
        # Create the Text menu.
        action_group.add_actions([
            ("text_menu", None, "_Text"),
            ("save", Gtk.STOCK_SAVE, "_Save to File...", "<Control>s", "Save to file", self.save_file),
            ("open", Gtk.STOCK_OPEN, "_Open from File...", "<Control>o", "Open from file", self.open_file)
        ])
        
        # Create the Options menu.
        action_group.add_actions([
            ("options_menu", None, "_Options"),
            ("options", None, "_Options...", "F2", None, self.options)
        ])
        
        # Create the Help menu.
        action_group.add_actions([
            ("help_menu", None, "_Help"),
            ("help", None, "_Help...", "F1", None, self.show_help),
            ("about", None, "_About...", "<Shift>F1", None, self.show_about),
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
        
        # Add the status bar.
        self.status_lbl = Gtk.Label("Not logged in")
        self.status_lbl.set_alignment(0, 0.5)
        grid.attach_next_to(self.status_lbl, scrolled_window, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Add the grid to the main window.
        self.add(grid)
        self.show_all()
        
        # Bind the events.
        self.connect("delete-event", self.delete_event)
        
        # Get the user login details, if they want that.
        if config["prompt_login"]:
            self.pastebin_login("ignore")
    
    
    def delete_event(self, widget, event):
        """Saves the window size."""
        
        # Get the current window size.
        height, width = self.get_size()
        
        # Save the window size.
        try:
            wins_file = open("%s/window_size" % main_dir, "w")
            wins_file.write("%d\n%d" % (height, width))
            wins_file.close()
        
        except IOError:
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error writing to the file.
            print("Error saving window size file (IOError).")
    
    
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
        
        # Set the default values.
        new_dlg.name_ent.set_text(config["default_name"])
        new_dlg.form_com.set_active(["None", "4CS", "6502 ACME Cross Assembler", "6502 Kick Assembler", "6502 TASM/64TASS", "ABAP", "ActionScript", "ActionScript 3", "Ada", "ALGOL 68", "Apache Log", "AppleScript", "APT Sources", "ARM", "ASM (NASM)", "ASP", "Asymptote", "autoconf", "Autohotkey", "AutoIt", "Avisynth", "Awk", "BASCOM AVR", "Bash", "Basic4GL", "BibTeX", "Blitz Basic", "BNF", "BOO", "BrainFuck", "C", "C for Macs", "C Intermediate Language", "C#", "C++", "C++ (with QT extensions)", "C: Loadrunner", "CAD DCL", "CAD Lisp", "CFDG", "ChaiScript", "Clojure", "Clone C", "Clone C++", "CMake", "COBOL", "CoffeeScript", "ColdFusion", "CSS", "Cuesheet", "D", "DCL", "DCPU-16", "DCS", "Delphi", "Delphi Prism (Oxygene)", "Diff", "DIV", "DOS", "DOT", "E", "ECMAScript", "Eiffel", "Email", "EPC", "Erlang", "F#", "Falcon", "FO Language", "Formula One", "Fortran", "FreeBasic", "FreeSWITCH", "GAMBAS", "Game Maker", "GDB", "Genero", "Genie", "GetText", "Go", "Groovy", "GwBasic", "Haskell", "Haxe", "HicEst", "HQ9 Plus", "HTML", "HTML 5", "Icon", "IDL", "INI file", "Inno Script", "INTERCAL", "IO", "J", "Java", "Java 5", "JavaScript", "jQuery", "KiXtart", "Latex", "LDIF", "Liberty BASIC", "Linden Scripting", "Lisp", "LLVM", "Loco Basic", "Logtalk", "LOL Code", "Lotus Formulas", "Lotus Script", "LScript", "Lua", "M68000 Assembler", "MagikSF", "Make", "MapBasic", "MatLab", "mIRC", "MIX Assembler", "Modula 2", "Modula 3", "Motorola 68000 HiSoft Dev", "MPASM", "MXML", "MySQL", "Nagios", "newLISP", "NullSoft Installer", "Oberon 2", "Objeck Programming Langua", "Objective C", "OCalm Brief", "OCaml", "Octave", "OpenBSD PACKET FILTER", "OpenGL Shading", "Openoffice BASIC", "Oracle 11", "Oracle 8", "Oz", "ParaSail", "PARI/GP", "Pascal", "PAWN", "PCRE", "Per", "Perl", "Perl 6", "PHP", "PHP Brief", "Pic 16", "Pike", "Pixel Bender", "PL/SQL", "PostgreSQL", "POV-Ray", "Power Shell", "PowerBuilder", "ProFTPd", "Progress", "Prolog", "Properties", "ProvideX", "PureBasic", "PyCon", "Python", "Python for S60", "q/kdb+", "QBasic", "R", "Rails", "REBOL", "REG", "Rexx", "Robots", "RPM Spec", "Ruby", "Ruby Gnuplot", "SAS", "Scala", "Scheme", "Scilab", "SdlBasic", "Smalltalk", "Smarty", "SPARK", "SPARQL", "SQL", "StoneScript", "SystemVerilog", "T-SQL", "TCL", "Tera Term", "thinBasic", "TypoScript", "Unicon", "UnrealScript", "UPC", "Urbi", "Vala", "VB.NET", "Vedit", "VeriLog", "VHDL", "VIM", "Visual Pro Log", "VisualBasic", "VisualFoxPro", "WhiteSpace", "WHOIS", "Winbatch", "XBasic", "XML", "Xorg Config", "XPP", "YAML", "Z80 Assembler", "ZXBasic"].index(config["default_format"]))
        new_dlg.expi_com.set_active(["Never", "10 Minutes", "1 Hour", "1 Day", "1 Week", "2 Weeks", "1 Month"].index(config["default_expiration"]))
        new_dlg.expo_com.set_active(["Public", "Unlisted", "Private"].index(config["default_exposure"]))
        
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
            
            try:
                
                # Send the paste.
                url = self.api.createPaste(api_paste_code = text, api_paste_name = name, api_paste_format = format_, api_paste_private = exposure, api_paste_expire_date = expire)
                
                # Show the url.
                show_alert_dialog(self, "Create Paste", "Paste has been successfully created, and can be found at the following URL:\n\n%s" % url)
            
            except urllib2.URLError:
                
                # Show an error if the paste could not be sent. This will occur if the user isn't connected to the internet.
                show_error_dialog(self, "Create Paste", "Paste could not be sent.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
        
        # Close the dialog.
        new_dlg.destroy()
    
    
    def get_paste(self, event, key = ""):
        """Gets an existing paste."""
        
        # If the key hasn't been specified, prompt the user.
        if not key:
        
            # Show the dialog.
            get_dlg = GetPasteDialog(self)
            response = get_dlg.run()
            
            # Get the key.
            key = get_dlg.key_ent.get_text()
            
            # Close the dialog.
            get_dlg.destroy()
        
            # If the user did not click OK, don't continue.
            if response != Gtk.ResponseType.OK:
                return
        
        try:
            # Get the paste.
            paste = self.api.getPasteRawOutput(api_paste_key = key)
        
        except urllib2.URLError:
            # Show an error if the paste could not be retrieved. This will occur if the user isn't connected to the internet.
            show_error_dialog(self, "Get Paste", "Paste could not be retrieved.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
        
        except PastebinHTTPErrorException:
            # Show an error if the paste could not be retreived. This will occur if the key is invalid.
            show_error_dialog(self, "Get Paste", "Paste could not be retrieved.\n\nThis likely means that an invalid paste key was specifed.")
            
        else:
            
            # Delete the current text and insert the new.
            self.text_buffer.delete(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter())
            self.text_buffer.insert(self.text_buffer.get_start_iter(), paste)
            
            # Set the cursor to the beginning of the sourceview.
            self.text_buffer.place_cursor(self.text_buffer.get_start_iter())
            
            # Guess the language, if the user wants that.
            if config["syntax_highlight"] and config["syntax_guess"]:
                pass
                
                # THIS IS A WORKAROUND WHERE IT REQUIRES A FILE TO DETECT A LANGUAGE
                # TODO: MAKE THIS NO LONGER REQUIRE A FILE
                
                # Create the temporary file.
                #temp_file = open("pastebingtk.temp", "w")
                #temp_file.write(paste)
                #temp_file.close()
                
                # Guess and set the language.
                #language = self.language_manager.guess_language("pastebingtk.temp", None)
                #print self.language_manager.get_language_ids()
                #print language
                #self.text_buffer.set_highlight_syntax(True)
                #self.text_buffer.set_language("python")
                
                # Cleanup the temporary file.
                #os.remove("pastebingtk.temp")
            
    
    def delete_paste(self, event):
        """Deletes an existing paste."""
        
        # The user must be logged in to do this.
        if not self.login:
            show_error_dialog(self, "Delete Paste", "Must be logged in to delete a paste.")
            return
        
        try:
            
            # Get the list of the user's pastes.
            pastes = self.api.listUserPastes()
        
        except PastebinNoPastesException:
            
            # If there are no pastes, tell the user.
            show_alert_dialog(self, "Delete Paste", "The currently logged in user has no pastes.")
            return
        
        except urllib2.URLError:
            
            show_error_dialog(self, "List User's Pastes", "Pastes could not be retrieved.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
            return
        
        # Create the list of data.
        data = []
        
        # Loop through the pastes and add the data.
        for i in pastes:
            
            new = []
            new.append(i["paste_title"])
            new.append(i["paste_key"])
            new.append(i["paste_format_long"])
            new.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i["paste_date"]))))
            data.append(new)
        
        # Show the dialog.
        del_dlg = DeletePasteDialog(self, data)
        response = del_dlg.run()
        
        # Get the selected item.
        model, treeiter = del_dlg.treeview.get_selection().get_selected()
        
        # Close the dialog.
        del_dlg.destroy()
        
        # If the user did not press OK, don't continue.
        if response != Gtk.ResponseType.OK:
            return
        
        # If nothing was selected, don't continue.
        if treeiter == None:
            return
        
        # Get the name and key.
        paste_name = model[treeiter][0]
        key = model[treeiter][1]
        
        try:
            
            # Get the paste.
            paste = self.api.deletePaste(api_paste_key = key)
        
        except urllib2.URLError:
            
            # Show an error if the paste could not be deleted. This will occur if the user isn't connected to the internet.
            show_error_dialog(self, "Delete Paste", "Paste could not be deleted.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
        
        except PastebinHTTPErrorException:
            
            # Show an error if the paste could not be deleted. This will occur if the key is invalid.
            show_error_dialog(self, "Delete Paste", "Paste could not be deleted.\n\nThis likely means that an invalid paste key was specifed.")
            
        else:
            
            if paste == True:
                show_alert_dialog(self, "Delete Paste", "%s was successfully deleted." % ("Paste \"%s\"" % paste_name if paste_name != "" else "Untitled paste"))
            
            else:
                show_error_dialog(self, "Delete Paste", "Paste could not be deleted.\n\nThis likely means that you do not have the ability to delete the specified paste.")
    
    
    def pastebin_login(self, event):
        """Logs the user in."""
        
        # Show the dialog.
        login_dlg = LoginDialog(self)
        if config["remember_username"]:
            login_dlg.name_ent.set_text(self.user_name)
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
                    self.status_lbl.set_text("Logged in as %s" % user_name)
                    show_alert_dialog(self, "Login", "Successfully logged in as %s." % user_name)
                
                except PastebinBadRequestException:
                    show_error_dialog(self, "Login", "Invalid username or password specified.\n\nNot logged in.")
                    self.login = False
                
                except urllib2.URLError:
                    show_error_dialog(self, "Login", "User authentication could not be sent.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
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
        self.status_lbl.set_text("Not logged in")
        show_alert_dialog(self, "Logout", "You are now logged out.")
    
    
    def list_users_pastes(self, event):
        """Gets the user's pastes"""
        
        exposure = {"0": "Public", "1": "Unlisted", "2": "Private"}
        
        # The user must be logged in to do this.
        if not self.login:
            show_error_dialog(self, "List User's Pastes", "Must be logged in to view a user's pastes.")
            return
        
        try:
            
            # Run the function to get the list of pastes.
            pastes = self.api.listUserPastes()
        
        except PastebinNoPastesException:
            
            # If there are no pastes, tell the user.
            show_alert_dialog(self, "List User's Pastes", "The currently logged in user has no pastes.")
            return
        
        except urllib2.URLError:
            
            show_error_dialog(self, "List User's Pastes", "Pastes could not be retrieved.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
            return
        
        # Create the list of data.
        data = []
        
        # Loop through the pastes and add the data.
        for i in pastes:
            
            new = []
            new.append(i["paste_title"])
            new.append(i["paste_key"])
            new.append(i["paste_format_long"])
            new.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i["paste_date"]))))
            if i["paste_expire_date"] == "0":
                new.append("Never")
            else:
                new.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i["paste_expire_date"]))))
            new.append(exposure[i["paste_private"]])
            size = int(i["paste_size"])
            if size < 1000:
                new.append("%d bytes" % size)
            elif size < 1000 * 1000:
                new.append("%d kB" % (size / 1000))
            else:
                new.append("%d MB" % (size / (1000 * 1000)))
            new.append(i["paste_hits"])
            new.append(i["paste_url"])
            
            data.append(new)
        
        # Create the dialog and get the response.
        list_dlg = ListPastesDialog(self, "%s's Pastes" % self.user_name, data)
        response = list_dlg.run()
        
        # Get the selected item.
        model, treeiter = list_dlg.treeview.get_selection().get_selected()
        
        # Close the dialog.
        list_dlg.destroy()
        
        # If the user clicked "Get Paste", load the selected paste.
        if response == 9:
            
            # If nothing was selected, don't continue.
            if treeiter == None:
                return
            
            # Get the key.
            key = model[treeiter][1]
            
            # Load the paste.
            self.get_paste(event = None, key = key)
    
    
    def list_trending_pastes(self, event):
        """Gets the trending pastes."""
        
        exposure = {"0": "Public", "1": "Unlisted", "2": "Private"}
        
        try:
            
            # Run the function to get the list of pastes.
            pastes = self.api.listTrendingPastes()
        
        except PastebinNoPastesException:
            
            # If there are no pastes, tell the user.
            show_alert_dialog(self, "List Trending Pastes", "There are no trending pastes.")
            return
        
        except urllib2.URLError:
            
            show_error_dialog(self, "List Trending Pastes", "Pastes could not be retrieved.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
            return
        
        # Create the list of data.
        data = []
        
        # Loop through the pastes and add the data.
        for i in pastes:
            
            new = []
            new.append(i["paste_title"])
            new.append(i["paste_key"])
            new.append(i["paste_format_long"])
            new.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i["paste_date"]))))
            if i["paste_expire_date"] == "0":
                new.append("Never")
            else:
                new.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i["paste_expire_date"]))))
            new.append(exposure[i["paste_private"]])
            size = int(i["paste_size"])
            if size < 1000:
                new.append("%d bytes" % size)
            elif size < 1000 * 1000:
                new.append("%d kB" % (size / 1000))
            else:
                new.append("%d MB" % (size / (1000 * 1000)))
            new.append(i["paste_hits"])
            new.append(i["paste_url"])
            
            data.append(new)
        
        # Create the dialog and get the response.
        list_dlg = ListPastesDialog(self, "Currently Trending Pastes", data)
        response = list_dlg.run()
        
        # Get the selected item.
        model, treeiter = list_dlg.treeview.get_selection().get_selected()
        
        # Close the dialog.
        list_dlg.destroy()
        
        # If the user clicked "Get Paste", load the selected paste.
        if response == 9:
            
            # If nothing was selected, don't continue.
            if treeiter == None:
                return
            
            # Get the key.
            key = model[treeiter][1]
            
            # Load the paste.
            self.get_paste(event = None, key = key)
    
    
    def get_user_details(self, event):
        """Gets the user's information and settings."""
        
        exposure = {"0": "Public", "1": "Unlisted", "2": "Private"}
        expiration = {"N": "Never", "10M": "10 Minutes", "1H": "1 Hour", "1D": "1 Day", "1W": "1 Week", "2W": "2 Weeks", "1M": "1 Month"}
        
        # The user must be logged in to do this.
        if not self.login:
            show_error_dialog(self, "Get User's Details", "Must be logged in to view a user's details.")
            return
        
        try:
            
            # Run the function to get the user's details
            info = self.api.getUserInfos()
        
        except urllib2.URLError:
            
            show_error_dialog(self, "Get User's Details", "Details could not be retrieved.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
            return
        
        # Get the user's details.
        data = self.api.getUserInfos()
        
        # Modify any fields, as necessary.
        data["Account Type"] = ["Normal", "Pro"][int(data["Account Type"])]
        data["Default Expiration"] = expiration[data["Default Expiration"]]
        data["Default Exposure"] = exposure[data["Default Exposure"]]
        
        # Convert dictionary to a list of lists.
        data2 = []
        for key, value in data.iteritems():
            data2.append([key, value])
        
        # Create the dialog and get the response.
        user_dlg = UserDetailsDialog(self, "%s's User Details" % self.user_name, data2)
        response = user_dlg.run()
        
        # Close the dialog.
        user_dlg.destroy()
        
        # If the user pressed "View Profile", open the profile in a web browser.
        if response == 9:
            
            webbrowser.open(data["User URL"])
    
    
    def save_file(self, event):
        """Saves the text to a file."""
        
        # Create the dialog.
        save_dlg = Gtk.FileChooserDialog("Save to File", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        save_dlg.set_do_overwrite_confirmation(True)
        
        # Get the response.
        response = save_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Get the filename.
            filename = save_dlg.get_filename()
            
            # Save the data.
            try:
                # Write to the specified file.
                data_file = open(filename, "w")
                data_file.write(self.text_buffer.get_text(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter(), False))
                data_file.close()
                
            except IOError:
                
                # Show the error message.
                # This only shows if the error occurred when writing to the file.
                print("Error writing to file (IOError).")
            
        # Close the dialog.
        save_dlg.destroy()
    
    
    def open_file(self, event):
        """Opens the text from a file."""
        
        # Create the dialog.
        open_dlg = Gtk.FileChooserDialog("Open from File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        open_dlg.set_do_overwrite_confirmation(True)
        
        # Get the response.
        response = open_dlg.run()
        if response == Gtk.ResponseType.OK:
            
            # Get the filename.
            filename = open_dlg.get_filename()
            
            # Read the data.
            try:
                
                # Read from the specified file.
                data_file = open(filename, "r")
                data = data_file.read()
                data_file.close()
                
            except IOError:
                
                # Show the error message.
                # This only shows if the error occurred when reading from the file.
                print("Error reading from file (IOError).")
            
            # Delete the old text and insert the new.
            self.text_buffer.delete(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter())
            self.text_buffer.insert_at_cursor(data)
            
        # Close the dialog.
        open_dlg.destroy()
    
    
    def options(self, event):
        """Shows the Options dialog."""
        
        global config
        
        # Create the dialog.
        opt_dlg = OptionsDialog(self, config)
        
        # Get the response.
        response = opt_dlg.run()
        
        # If the user pressed OK:
        if response == Gtk.ResponseType.OK:
            
            # Get the values.
            login = opt_dlg.log_chk.get_active()
            username = opt_dlg.user_chk.get_active()
            restore_window = opt_dlg.win_chk.get_active()
            confirm_exit = opt_dlg.exit_chk.get_active()
            def_name = opt_dlg.name_ent.get_text()
            def_format = opt_dlg.form_com.get_active_text()
            def_expire = opt_dlg.expi_com.get_active_text()
            def_expo = opt_dlg.expo_com.get_active_text()
            line_num = opt_dlg.lin_chk.get_active()
            syntax = opt_dlg.syn_chk.get_active()
            syntax_guess = opt_dlg.asyn_chk.get_active()
            syntax_def = opt_dlg.dsyn_ent.get_text()
            dev_key = opt_dlg.devk_ent.get_text()
            
            # Set the values.
            config["prompt_login"] = login
            config["remember_username"] = username
            config["restore_window"] = restore_window
            config["confirm_exit"] = confirm_exit
            config["default_name"] = def_name
            config["default_format"] = def_format
            config["default_expiration"] = def_expire
            config["default_exposure"] = def_expo
            config["line_numbers"] = line_num
            config["syntax_highlight"] = syntax
            config["syntax_guess"] = syntax_guess
            config["syntax_default"] = syntax_def
            config["dev_key"] = dev_key
            
            # Update anything that could have changed.
            self.text_view.set_show_line_numbers(line_num)
        
        # Close the dialog.
        opt_dlg.destroy()
    
    
    def show_help(self, event):
        """Shows the help."""
        
        # Open the help in the user's web browser.
        webbrowser.open("resources/help/help.html")
    
    
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
    
    
    def exit(self, x, y):
        """Closes the application."""
        
        # Confirm that the user wants to quit, if they want that.
        if config["confirm_exit"]:
            
            conf_exit = show_question_dialog(self, "Exit", "Are you sure you want to exit?")
            
            if conf_exit != Gtk.ResponseType.OK:
                return True
        
        # Save the configuration.
        try:
            # Save the configuration file.
            config_file = open("%s/config" % main_dir, "w")
            json.dump(config, config_file)
            config_file.close()
            
        except IOError:
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error writing to the file.
            print("Error saving configuration file (IOError).")
        
        except (TypeError, ValueError):
            # Show the error message if something happened, but continue.
            # This one is shown if there was an error with the data type.
            print("Error saving configuration file (TypeError or ValueError).")
        
        # Save the last username, if the user wants that.
        if config["remember_username"]:
            
            try:
                # Save the username.
                user_file = open("%s/username" % main_dir, "w")
                user_file.write(self.user_name)
                user_file.close()
            
            except IOError:
                # Show the error message if something happened, but continue.
                # This one is shown if there was an error writing to the file.
                print("Error saving username file (IOError).")
        
        # Close the application.
        Gtk.main_quit()


# If there are no parameters, show the GUI.
if  __name__ == "__main__" and len(sys.argv) == 1:
    
    # Create the application.
    win = PastebinGTK()
    win.connect("delete-event", win.exit)
    win.show_all()
    Gtk.main()

# If there are parameters specified, run the application from the command line.
elif __name__ == "__main__" and len(sys.argv) > 1:
    
    # Make sure the usage is correct.
    if len(sys.argv) < 3:
        print("Usage: pastebincl [mode] [text/file/key] [[title] [format] [exposure] [expiration]]")
        sys.exit()
    
    # Uploading text:
    if sys.argv[1] == "upload" or sys.argv[1] == "uploadfile":
        url = command_line.upload(sys.argv, config["dev_key"])
        print("Paste uploaded: %s" % url)
    
    # Downloading text:
    elif sys.argv[1] == "download" or sys.argv[1] == "downloadfile":
        text = command_line.download(sys.argv, config["dev_key"])
        if sys.argv[1] == "download":
            print(text)
        else:
            open(sys.argv[3], "w").write(text)
    
    # Other command:
    else:
        print("Usage: pastebincl [mode] [text/file/key] [[title] [format] [exposure] [expiration]]")
