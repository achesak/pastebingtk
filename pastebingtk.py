# -*- coding: utf-8 -*-


################################################################################

# PastebinGTK
# Version 1.3

# PastebinGTK is a desktop client for pastebin.com.

# Released under the MIT open source license:
license_text = """
Copyright (c) 2013-2016 Adam Chesak

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


# Import GTK and Python lib modules.
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GtkSource", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GtkSource
import sys
import os
import webbrowser
import urllib2
import time
import json
import webbrowser

# Try to import BeautifulSoup. This is needed for getting the list
# of most recently created pastes. If the user doesn't have it installed,
# fail as gracefully as possible.
try:
    from bs4 import BeautifulSoup
    bs4_installed = True
except ImportError:
    bs4_installed = False

# Tell Python not to create bytecode files, as they mess with the git repo.
# This line can be removed be the user, if desired.
sys.dont_write_bytecode = True

# Import the application modules
import resources.launch as launch
import resources.io as io

# Import the dialogs.
from resources.dialogs.login_dialog import LoginDialog
from resources.dialogs.create_dialog import CreatePasteDialog
from resources.dialogs.get_dialog import GetPasteDialog
from resources.dialogs.delete_dialog import DeletePasteDialog
from resources.dialogs.list_user_dialog import ListPastesDialog, ListPastesDialog2
from resources.dialogs.list_recent_dialog import ListRecentDialog
from resources.dialogs.user_details_dialog import UserDetailsDialog
from resources.dialogs.options_dialog import OptionsDialog
from resources.dialogs.misc_dialogs import show_alert_dialog, show_error_dialog, show_question_dialog

# Import the pastebin API wrapper.
import resources.python_pastebin.pastebin_api as pastebin_api
import resources.python_pastebin.pastebin_extras as pastebin_extras
from resources.python_pastebin.pastebin_dicts import FORMATS, EXPIRE, EXPOSURE


class PastebinGTK(Gtk.Window):

    def __init__(self):
        """Creates the application."""
        
        # Application data:
        self.main_dir = launch.get_main_dir()
        self.config = io.get_config(self.main_dir)
        self.application_data = io.get_application_data(self.main_dir)
        self.last_width = self.application_data["width"]
        self.last_height = self.application_data["height"]

        # UI data:
        self.ui_data = io.get_ui_data()
        self.menu_data = io.get_menu_data()
        
        # Variables for remembering user data:
        self.user_name = self.application_data["username"]
        self.user_key = ""
        self.dev_key = self.config["dev_key"]
        self.login = False
        
        # Show the interface.
        self.create_ui()
        
        # Get the user login details, if they want that.
        if self.config["prompt_login"]:
            self.pastebin_login("ignore")
    
    
    def create_ui(self):
        """Builds the interface."""
        
        # Create the window.
        Gtk.Window.__init__(self, title = self.ui_data["title"])
        self.set_default_size(self.last_width, self.last_height)
        self.set_icon_from_file(self.ui_data["icon_path"])
        
        # Build the UI.
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        self.text_view = GtkSource.View.new()
        self.language_manager = GtkSource.LanguageManager.new()
        self.text_buffer = self.text_view.get_buffer()
        scrolled_window.add(self.text_view)
        
        # Set the font to the system default monospaced.
        self.font = Pango.FontDescription("Courier New")
        self.text_view.modify_font(self.font)
        
        # Show line numbers, if the user wants that.
        if self.config["line_numbers"]:
            self.text_view.set_show_line_numbers(True)
        
        # Create the menus.
        action_group = Gtk.ActionGroup("actions")
        action_group.add_actions([
            ("pastebin_menu", None, "_Pastebin"),
            ("create_paste", Gtk.STOCK_GO_UP, "_Create Paste...", "<Control>n", "Create a new paste", self.create_paste),
            ("get_paste", Gtk.STOCK_GO_DOWN, "_Get Paste...", "<Control>g", "Get a paste", self.get_paste),
            ("delete_paste", Gtk.STOCK_DELETE, "_Delete Paste...", "<Control>d", "Delete a paste", self.delete_paste),
            ("get_paste_info", None, "Get Paste _Info...", "<Control>i", None, self.get_paste_info),
            ("list_trending_pastes", None, "List _Trending Pastes...", "<Control>t", None, lambda x: self.list_pastes(source = "trending")),
            ("list_users_pastes", None, "List _User's Pastes...", "<Control>u", None, lambda x: self.list_pastes(source = "user")),
            ("list_recent_pastes", None, "List _Recent Pastes...", "<Control>r", None, self.list_recent),
            ("options", None, "_Options...", "F2", None, self.options),
            ("quit", Gtk.STOCK_QUIT, "_Quit", "<Control>q", None, lambda x: self.exit("ignore", "this"))
        ])
        action_group.add_actions([
            ("user_menu", None, "_User"),
            ("login", None, "_Login...", "<Control>l", None, self.pastebin_login),
            ("logout", None, "Log_out...", "<Shift><Control>l", None, self.pastebin_logout),
            ("user_details", None, "Get Account _Details...", None, None, self.get_user_details)
        ])
        action_group.add_actions([
            ("text_menu", None, "_Text"),
            ("save", Gtk.STOCK_SAVE, "_Save to File...", "<Control>s", "Save to file", self.save_file),
            ("open", Gtk.STOCK_OPEN, "_Open from File...", "<Control>o", "Open from file", self.open_file)
        ])
        action_group.add_actions([
            ("help_menu", None, "_Help"),
            ("about", None, "_About...", "F1", None, self.show_about)
        ])
        
        # Set up the menus.
        ui_manager = Gtk.UIManager()
        ui_manager.add_ui_from_string(self.menu_data)
        accel_group = ui_manager.get_accel_group()
        self.add_accel_group(accel_group)
        ui_manager.insert_action_group(action_group)
        
        # Set up and show the interface.
        grid = Gtk.Grid()
        menubar = ui_manager.get_widget("/menubar")
        grid.add(menubar)
        toolbar = ui_manager.get_widget("/toolbar")
        grid.attach_next_to(toolbar, menubar, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(scrolled_window, toolbar, Gtk.PositionType.BOTTOM, 1, 1)
        self.status_lbl = Gtk.Label("Not logged in")
        self.status_lbl.set_alignment(0, 0.5)
        grid.attach_next_to(self.status_lbl, scrolled_window, Gtk.PositionType.BOTTOM, 1, 1)
        self.add(grid)
        self.show_all()
        
        # Bind the events.
        self.connect("delete-event", self.delete_event)
    
    
    def delete_event(self, widget, event):
        """Saves the window size."""
        
        # Save the current window size.
        width, height = self.get_size()
        io.save_application_data(self.main_dir, self.config, width, height, self.user_name)
    
    
    def create_paste(self, event):
        """Creates a new paste."""
        
        # Get the text.
        text = self.text_buffer.get_text(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter(), False)
        
        # If there's no text, don't create the paste.
        if not text:
            show_error_dialog(self, "Create Paste", "No text entered.")
            return
        
        # Get the name, format, expiration, and exposure for the paste.
        new_dlg = CreatePasteDialog(self)
        new_dlg.name_ent.set_text(self.config["default_name"])
        new_dlg.form_com.set_active(["None", "4CS", "6502 ACME Cross Assembler", "6502 Kick Assembler", "6502 TASM/64TASS", "ABAP", "ActionScript", "ActionScript 3", "Ada", "ALGOL 68", "Apache Log", "AppleScript", "APT Sources", "ARM", "ASM (NASM)", "ASP", "Asymptote", "autoconf", "Autohotkey", "AutoIt", "Avisynth", "Awk", "BASCOM AVR", "Bash", "Basic4GL", "BibTeX", "Blitz Basic", "BNF", "BOO", "BrainFuck", "C", "C for Macs", "C Intermediate Language", "C#", "C++", "C++ (with QT extensions)", "C: Loadrunner", "CAD DCL", "CAD Lisp", "CFDG", "ChaiScript", "Clojure", "Clone C", "Clone C++", "CMake", "COBOL", "CoffeeScript", "ColdFusion", "CSS", "Cuesheet", "D", "DCL", "DCPU-16", "DCS", "Delphi", "Delphi Prism (Oxygene)", "Diff", "DIV", "DOS", "DOT", "E", "ECMAScript", "Eiffel", "Email", "EPC", "Erlang", "F#", "Falcon", "FO Language", "Formula One", "Fortran", "FreeBasic", "FreeSWITCH", "GAMBAS", "Game Maker", "GDB", "Genero", "Genie", "GetText", "Go", "Groovy", "GwBasic", "Haskell", "Haxe", "HicEst", "HQ9 Plus", "HTML", "HTML 5", "Icon", "IDL", "INI file", "Inno Script", "INTERCAL", "IO", "J", "Java", "Java 5", "JavaScript", "jQuery", "KiXtart", "Latex", "LDIF", "Liberty BASIC", "Linden Scripting", "Lisp", "LLVM", "Loco Basic", "Logtalk", "LOL Code", "Lotus Formulas", "Lotus Script", "LScript", "Lua", "M68000 Assembler", "MagikSF", "Make", "MapBasic", "MatLab", "mIRC", "MIX Assembler", "Modula 2", "Modula 3", "Motorola 68000 HiSoft Dev", "MPASM", "MXML", "MySQL", "Nagios", "newLISP", "NullSoft Installer", "Oberon 2", "Objeck Programming Langua", "Objective C", "OCalm Brief", "OCaml", "Octave", "OpenBSD PACKET FILTER", "OpenGL Shading", "Openoffice BASIC", "Oracle 11", "Oracle 8", "Oz", "ParaSail", "PARI/GP", "Pascal", "PAWN", "PCRE", "Per", "Perl", "Perl 6", "PHP", "PHP Brief", "Pic 16", "Pike", "Pixel Bender", "PL/SQL", "PostgreSQL", "POV-Ray", "Power Shell", "PowerBuilder", "ProFTPd", "Progress", "Prolog", "Properties", "ProvideX", "PureBasic", "PyCon", "Python", "Python for S60", "q/kdb+", "QBasic", "R", "Rails", "REBOL", "REG", "Rexx", "Robots", "RPM Spec", "Ruby", "Ruby Gnuplot", "SAS", "Scala", "Scheme", "Scilab", "SdlBasic", "Smalltalk", "Smarty", "SPARK", "SPARQL", "SQL", "StoneScript", "SystemVerilog", "T-SQL", "TCL", "Tera Term", "thinBasic", "TypoScript", "Unicon", "UnrealScript", "UPC", "Urbi", "Vala", "VB.NET", "Vedit", "VeriLog", "VHDL", "VIM", "Visual Pro Log", "VisualBasic", "VisualFoxPro", "WhiteSpace", "WHOIS", "Winbatch", "XBasic", "XML", "Xorg Config", "XPP", "YAML", "Z80 Assembler", "ZXBasic"].index(self.config["default_format"]))
        new_dlg.expi_com.set_active(["Never", "10 Minutes", "1 Hour", "1 Day", "1 Week", "2 Weeks", "1 Month"].index(self.config["default_expiration"]))
        new_dlg.expo_com.set_active(["Public", "Unlisted", "Private"].index(self.config["default_exposure"]))
        response = new_dlg.run()
        name = new_dlg.name_ent.get_text()
        format_ = new_dlg.form_com.get_active_text()
        expire = new_dlg.expi_com.get_active_text()
        exposure = new_dlg.expo_com.get_active_text()
        new_dlg.destroy()
        
        # Get the paste values.
        format_ = FORMATS[format_]
        expire = EXPIRE[expire]
        exposure = EXPOSURE[exposure]
        
        # If the user isn't logged in, they can't create private pastes.
        if not self.user_key and exposure == 2:
            show_alert_dialog(self, "Create Paste", "Anonymous users cannot create private pastes.")
            return
        
        # If the user clicked OK:
        if response == Gtk.ResponseType.OK:
            
            try:
                # Send the paste.
                url = pastebin_api.create_paste(self.config["dev_key"], data = text, name = name, format_ = format_, private = exposure, expire = expire, userkey = self.user_key)
                
                # Check for the spam filter, if the user wants that.
                caught_spam = False
                if self.config["check_spam"]:
                    
                    try:
                        paste = pastebin_api.get_paste(pastekey = url.rsplit("/", 1)[-1])
                
                    except urllib2.URLError:
                        pass
                    
                    else:
                        # Check if the paste doesn't match.
                        if paste != text:
                            caught_spam = True
                
                
                # Show the url.
                if not caught_spam or exposure == 2:
                    show_alert_dialog(self, "Create Paste", "Paste has been successfully created, and can be found at the following URL:\n\n%s" % url)
                else:
                    show_alert_dialog(self, "Create Paste", "Paste triggered automatic spam detection filter. Verify that you are not a bot by filling out the captcha at the following URL:\n\n%s" % url)
            
            except urllib2.URLError:
                # Show an error if the paste could not be sent. This will occur if the user isn't connected to the internet.
                show_error_dialog(self, "Create Paste", "Paste could not be sent.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
    
    
    def get_paste(self, event, key = ""):
        """Gets an existing paste."""
        
        # If the key hasn't been specified, prompt the user.
        if not key:
        
            # Get the key.
            get_dlg = GetPasteDialog(self)
            response = get_dlg.run()
            key = get_dlg.key_ent.get_text()
            if key.startswith("http://") or key.startswith("www.") or key.startswith("pastebin"):
                key = key.rsplit("/", 1)[-1]
            get_dlg.destroy()
        
            # If the user did not click OK, don't continue.
            if response != Gtk.ResponseType.OK:
                return
        
        try:
            # Get the paste.
            paste = pastebin_api.get_paste(pastekey = key)
        
        except urllib2.URLError:
            # Show an error if the paste could not be retrieved. This will occur if the user isn't connected to the internet.
            show_error_dialog(self, "Get Paste", "Paste could not be retrieved.\n\nThis likely means that an invalid paste was specified, you are not connected to the internet, or the pastebin.com website is down.")
        
        else:
            
            # Did we try to load a private paste?
            if paste == "Error, this is a private paste. If this is your private paste, please login to Pastebin first.":
                show_alert_dialog(self, "Get Paste", "Due to API restrictions PastebinGTK is unable to load private pastes.")
                return
            
            # Delete the current text and insert the new.
            self.text_buffer.delete(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter())
            self.text_buffer.insert(self.text_buffer.get_start_iter(), paste)
            self.text_buffer.place_cursor(self.text_buffer.get_start_iter())
        
    
    def delete_paste(self, event):
        """Deletes an existing paste."""
        
        # The user must be logged in to do this.
        if not self.login:
            show_error_dialog(self, "Delete Paste", "Must be logged in to delete a paste.")
            return
        
        # Get the list of the user's pastes.
        try:
            pastes = pastebin_api.list_users_pastes(self.config["dev_key"], self.user_key)
            
            # If the user has no pastes, don't continue.
            if len(pastes) == 0:
                show_alert_dialog(self, "Delete Paste", "The currently logged in user has no pastes.")
                return
        
        except urllib2.URLError:
            show_error_dialog(self, "Delete Paste", "Pastes could not be retrieved.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
            return
        
        # Create the list of data.
        data = []
        for i in pastes:
            new = []
            new.append(i["title"])
            new.append(i["key"])
            new.append(i["format_long"])
            new.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i["expire_date"]))))
            data.append(new)
        
        # Get the paste to delete.
        del_dlg = DeletePasteDialog(self, data)
        response = del_dlg.run()
        model, treeiter = del_dlg.treeview.get_selection().get_selected()
        del_dlg.destroy()
        
        # If the user did not press OK or nothing was selected, don't continue.
        if response != Gtk.ResponseType.OK or treeiter == None:
            return
        
        # Get the name and key.
        paste_name = model[treeiter][0]
        key = model[treeiter][1]
        
        # Ask the user for confirmation.
        del_conf = show_question_dialog(self, "Delete Paste", "Are you sure you want to delete the selected paste?")
        if del_conf != Gtk.ResponseType.OK:
            return
        
        try:
            # Get the paste.
            paste = pastebin_api.delete_paste(self.config["dev_key"], self.user_key, key)
        
        except urllib2.URLError:
            # Show an error if the paste could not be deleted. This will occur if the user isn't connected to the internet.
            show_error_dialog(self, "Delete Paste", "Paste could not be deleted.\n\nThis likely means that an invalid paste was specified, you are not connected to the internet, or the pastebin.com website is down.")
        
        else:
            if paste == "Paste Removed":
                show_alert_dialog(self, "Delete Paste", "%s was successfully deleted." % ("Paste \"%s\"" % paste_name if paste_name != "" else "Untitled paste"))
            else:
                show_error_dialog(self, "Delete Paste", "Paste could not be deleted.\n\nThis likely means that you do not have the ability to delete the specified paste.")
    
    
    def get_paste_info(self, event):
        """Gets info on a provided paste."""
        
        # If BeautifulSoup is not installed, this feature won't work.
        if not bs4_installed:
            show_alert_dialog(self, "Get Paste Info", "This feature requires the BeautifulSoup 4 HTML parsing library to be installed.")
            return
        
        # Get the key.
        get_dlg = GetPasteDialog(self, title = "Get Paste Info")
        response = get_dlg.run()
        key = get_dlg.key_ent.get_text()
        if key.startswith("http://") or key.startswith("www.") or key.startswith("pastebin"):
            key = key.rsplit("/", 1)[-1]
        get_dlg.destroy()
    
        # If the user did not click OK, don't continue.
        if response != Gtk.ResponseType.OK:
            return
        
        # Get the paste info.
        try:
            info = pastebin_extras.get_paste_info("http://pastebin.com/" + key)
        except urllib2.URLError:
            show_error_dialog(self, "Get Paste Info", "Paste could not be retrieved.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
            return
        
        data = [
            ["Name", info["name"]],
            ["Uploaded by", info["username"]],
            ["Views", info["views"]],
            ["Upload time", info["uploaded"]],
            ["Delete time", info["delete"]]
        ]
        
        # Show the paste info.
        paste_dlg = UserDetailsDialog(self, "Paste Info for " + key, data)
        response = paste_dlg.run()
        paste_dlg.destroy()
        
    
    def pastebin_login(self, event):
        """Logs the user in."""
        
        # If the user is alread logged in, don't continue.
        if self.login:
            show_alert_dialog(self, "Login", "Already logged in as %s." % self.user_name)
            return
        
        # Get the username and password.
        login_dlg = LoginDialog(self)
        if self.config["remember_username"]:
            login_dlg.name_ent.set_text(self.user_name)
        response = login_dlg.run()
        user_name = login_dlg.name_ent.get_text()
        password = login_dlg.pass_ent.get_text()
        
        # If the user clicked OK:
        if response == Gtk.ResponseType.OK:
            
            # If the username and password are valid, get the user key
            if user_name != "" and password != "":
                
                try:
                    self.user_key = pastebin_api.create_user_key(self.config["dev_key"], user_name, password)
                    if self.user_key == "Bad API request, invalid login":
                        raise TypeError  # Bit of a hack here...
                    self.user_name = user_name
                    self.login = True
                    self.status_lbl.set_text("Logged in as %s." % user_name)
                    show_alert_dialog(self, "Login", "Successfully logged in as %s." % user_name)
                
                except TypeError:
                    self.user_key = ""
                    show_error_dialog(self, "Login", "Invalid username or password specified.\n\nNot logged in.")
                
                except urllib2.URLError:
                    show_error_dialog(self, "Login", "User authentication could not be sent.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
                    self.login = False
            
            else:
                show_error_dialog(self, "Login", "No %s entered.\n\nNot logged in." % "username" if user_name == "" else "password")
                self.login = False
        
        else:
            self.login = False
            
        # Close the dialog.
        login_dlg.destroy()
    
    
    def pastebin_logout(self, event):
        """Logs the user out."""
        
        self.login = False
        self.user_key = ""
        self.status_lbl.set_text("Not logged in")
        show_alert_dialog(self, "Logout", "You are now logged out.")
    
    
    def list_pastes(self, source):
        """Get's the user's pastes or the currently trending pastes."""
        
        exposure = {"0": "Public", "1": "Unlisted", "2": "Private"}
        title1 = "List User's Pastes" if source == "user" else "List Trending Pastes"
        title2 = "%s's Pastes" % self.user_name if source == "user" else "Trending Pastes"
        
        # If getting the user's pastes, the user must be logged in.
        if source == "user" and not self.login:
            show_error_dialog(self, title1, "Must be logged in to view a user's pastes.")
            return
        
        try:
            # Get the list of pastes.
            if source == "user":
                pastes = pastebin_api.list_users_pastes(self.dev_key, self.user_key, results_limit = int(self.config["pastes_retrieve"]))
            else:
                pastes = pastebin_api.list_trending_pastes(self.dev_key)
        
        except urllib2.URLError:
            show_error_dialog(self, title1, "Pastes could not be retrieved.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
            return
        
        if len(pastes) == 0:
            # If there are no pastes, tell the user.
            show_alert_dialog(self, title1, "The currently logged in user has no pastes.")
            return
        
        # Create the list of data.
        data = []
        for i in pastes:
            new = []
            if not i["title"]:
                new.append("Untitled")
            else:
                new.append(i["title"])
            new.append(i["key"])
            if source == "user":
                new.append(i["format_long"])
            new.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i["date"]))))
            if i["expire_date"] == "0":
                new.append("Never")
            else:
                new.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i["expire_date"]))))
            new.append(exposure[i["private"]])
            size = int(i["size"])
            if size < 1000:
                new.append("%d bytes" % size)
            elif size < 1000 * 1000:
                new.append("%d kB" % (size / 1000))
            else:
                new.append("%d MB" % (size / (1000 * 1000)))
            new.append(i["hits"])
            new.append(i["url"])
            
            data.append(new)
        
        # Show the list of pastes.
        if source == "user":
            list_dlg = ListPastesDialog(self, title2, data)
        else:
            list_dlg = ListPastesDialog2(self, title2, data)
        response = list_dlg.run()
        model, treeiter = list_dlg.treeview.get_selection().get_selected()
        list_dlg.destroy()
        
        # If the user clicked "Get Paste", load the selected paste.
        if response == 9:
            
            # If nothing was selected, don't continue.
            if treeiter == None:
                return
            
            # Can't load private pastes due to API restrictions.
            if (source == "user" and model[treeiter][5] == "Private") or \
               (source == "trending" and model[treeiter][4] == "Private"):
                show_alert_dialog(self, title2, "Due to API restrictions PastebinGTK is unable to load private pastes.")
                return
            
            # Get the key and load the paste.
            key = model[treeiter][1]
            self.get_paste(event = None, key = key)
    
    
    def list_recent(self, event):
        """Lists recently created pastes."""
        
        # If BeautifulSoup is not installed, this feature won't work.
        if not bs4_installed:
            show_alert_dialog(self, "List Recent Pastes", "This feature requires the BeautifulSoup 4 HTML parsing library to be installed.")
            return
        
        # Get the list of most recently created pastes.
        try:
            pastes = pastebin_extras.list_recent_pastes()
        
        except urllib2.URLError:
            show_error_dialog(self, "List Recent Pastes", "Pastes could not be retrieved.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
            return
        
        # Reformat the data into something the dialog can use.
        data = []
        for i in pastes:
            row = [
                i["name"], i["key"], i["format"] if i["format"] != "-" else "Unknown", i["time_created"], i["link"]
            ]
            data.append(row)
        
        # Show the list of pastes.
        list_dlg = ListRecentDialog(self, "List Recent Pastes", data)
        response = list_dlg.run()
        model, treeiter = list_dlg.treeview.get_selection().get_selected()
        list_dlg.destroy()
        
        # If the user clicked "Get Paste", load the selected paste.
        if response == 9:
            
            # If nothing was selected, don't continue.
            if treeiter == None:
                return
            
            # Get the key and load the paste.
            key = model[treeiter][1]
            self.get_paste(event = None, key = key)
    
    
    def get_user_details(self, event):
        """Gets the user's information and settings."""
        
        ACCOUNT_PRIVACY = {"0": "Public",
                           "1": "Unlisted",
                           "2": "Private"
        }
        ACCOUNT_TYPE = {"0": "Normal",
                        "1": "Pro"
        }
        
        # The user must be logged in to do this.
        if not self.login:
            show_error_dialog(self, "Get Account Details", "Must be logged in to view a user's details.")
            return
        
        try:
            # Run the function to get the user's details
            info = pastebin_api.get_user_info(self.dev_key, self.user_key)        
        except urllib2.URLError:
            show_error_dialog(self, "Get Account Details", "Details could not be retrieved.\n\nThis likely means that you are not connected to the internet, or the pastebin.com website is down.")
            return
        
        # Format the data into the way the dialog uses it.
        data = [
            ["Username", info["name"]],
            ["User URL", "http://pastebin.com/u/" + info["name"]]
        ]
        if "email" in info:
            data.append(["Email", info["email"]])
        if "website" in info:
            data.append(["Website", info["website"]])
        if "location" in info:
            data.append(["Location", info["location"]])
        if "avatar_url" in info:
            data.append(["Avatar URL", info["avatar_url"]])
        if "account_type" in info:
            data.append(["Account Type", ACCOUNT_TYPE[info["account_type"]]])
        if "format_short" in info:
            data.append(["Default Format", info["format_short"]])
        if "expiration" in info:
            data.append(["Default Expiration", info["expiration"]])
        if "private" in info:
            data.append(["Default Exposure", ACCOUNT_PRIVACY[info["private"]]])
        
        # If Beautiful Soup is installed, get some extra info.
        if bs4_installed:
			extra_info = pastebin_extras.get_user_details_extra(self.user_name)
			data += extra_info
        
        # Show the user's details.
        user_dlg = UserDetailsDialog(self, "%s's Account Details" % self.user_name, data)
        response = user_dlg.run()
        user_dlg.destroy()
        
        # If the user pressed "View Profile", open the profile in a web browser.
        if response == 9:
            webbrowser.open(data[1][1])
    
    
    def save_file(self, event):
        """Saves the text to a file."""
        
        # Get the filename.
        save_dlg = Gtk.FileChooserDialog("Save to File", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        save_dlg.set_do_overwrite_confirmation(True)
        response = save_dlg.run()
        filename = save_dlg.get_filename()
        save_dlg.destroy()
        
        # If the user clicked OK:
        if response == Gtk.ResponseType.OK:
            
            # Save the data.
            io.save_file(filename, self.text_buffer.get_text(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter(), False))
    
    
    def open_file(self, event):
        """Opens the text from a file."""
        
        # Get the filename.
        open_dlg = Gtk.FileChooserDialog("Open from File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        open_dlg.set_do_overwrite_confirmation(True)
        response = open_dlg.run()
        filename = open_dlg.get_filename()
        open_dlg.destroy()
        
        # If the user clicked OK:
        if response == Gtk.ResponseType.OK:
            
            # Read the data.
            data = io.read_file(filename)
            
            # Delete the old text and insert the new.
            self.text_buffer.delete(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter())
            self.text_buffer.insert_at_cursor(data)
            self.text_buffer.place_cursor(self.text_buffer.get_start_iter())
        
    
    def options(self, event):
        """Shows the Options dialog."""
        
        # Get the new options.
        opt_dlg = OptionsDialog(self, self.config)
        response = opt_dlg.run()
        
        # If the user pressed OK:
        if response == Gtk.ResponseType.OK:
            
            # Get the values.
            login = opt_dlg.log_chk.get_active()
            username = opt_dlg.user_chk.get_active()
            restore_window = opt_dlg.win_chk.get_active()
            confirm_exit = opt_dlg.exit_chk.get_active()
            check_spam = opt_dlg.spam_chk.get_active()
            pastes_retrieve = opt_dlg.lnum_sbtn.get_value()
            def_name = opt_dlg.name_ent.get_text()
            def_format = opt_dlg.form_com.get_active_text()
            def_expire = opt_dlg.expi_com.get_active_text()
            def_expo = opt_dlg.expo_com.get_active_text()
            line_num = opt_dlg.lin_chk.get_active()
            dev_key = opt_dlg.devk_ent.get_text()
            
            # Set the values.
            self.config["prompt_login"] = login
            self.config["remember_username"] = username
            self.config["restore_window"] = restore_window
            self.config["confirm_exit"] = confirm_exit
            self.config["check_spam"] = check_spam
            self.config["pastes_retrieve"] = pastes_retrieve
            self.config["default_name"] = def_name
            self.config["default_format"] = def_format
            self.config["default_expiration"] = def_expire
            self.config["default_exposure"] = def_expo
            self.config["line_numbers"] = line_num
            self.config["dev_key"] = dev_key
            
            # Update anything that could have changed.
            self.text_view.set_show_line_numbers(line_num)
        
        # Close the dialog.
        opt_dlg.destroy()
    
    
    def show_about(self, event):
        """Shows the About dialog."""
        
        # Load the icon.
        img_file = open(self.ui_data["icon_path"], "rb")
        img_bin = img_file.read()
        img_file.close()
        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        loader.write(img_bin)
        loader.close()
        pixbuf = loader.get_pixbuf()
        
        # Create the dialog.
        about_dlg = Gtk.AboutDialog()
        
        # Set the details.
        about_dlg.set_title("About " + self.ui_data["title"])
        about_dlg.set_program_name(self.ui_data["title"])
        about_dlg.set_logo(pixbuf)
        about_dlg.set_version(self.ui_data["version"])
        about_dlg.set_comments("PastebinGTK is a desktop client for pastebin.com.")
        about_dlg.set_copyright("Copyright (c) 2013-2016 Adam Chesak")
        about_dlg.set_authors(["Adam Chesak <achesak@yahoo.com>"])
        about_dlg.set_license(license_text)
        about_dlg.set_website("http://poultryandprogramming.wordpress.com/")
        about_dlg.set_website_label("http://poultryandprogramming.wordpress.com/")
        
        # Show the dialog.
        about_dlg.show_all()
    
    
    def exit(self, x, y):
        """Closes the application."""
        
        # Confirm that the user wants to quit:
        if self.config["confirm_exit"]:
            conf_exit = show_question_dialog(self, "Exit", "Are you sure you want to exit?")
            if conf_exit != Gtk.ResponseType.OK:
                return True
        
        # Save the configuration.
        io.save_config(self.main_dir, self.config)
        
        # Close the application.
        Gtk.main_quit()


if  __name__ == "__main__" and len(sys.argv) == 1:
    
    # Create the application.
    win = PastebinGTK()
    win.connect("delete-event", win.exit)
    win.show_all()
    Gtk.main()
