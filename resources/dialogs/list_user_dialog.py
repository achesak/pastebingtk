# -*- coding: utf-8 -*-


# This file defines the paste list view dialog.


# Import GTK for the dialog.
from gi.repository import Gtk

# Import application modules.
from resources.constants import *


class ListUserPastesDialog(Gtk.Dialog):
    """Shows the list dialog."""
    def __init__(self, parent, title, data):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(1200, 500)
        self.get_btn = self.add_button("Get Paste", DialogResponse.GET_PASTE)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the columns for displaying the pastes.
        self.liststore = Gtk.ListStore(str, str, str, str, str, str, str, str, str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        name_text = Gtk.CellRendererText()
        name_col = Gtk.TreeViewColumn("Name", name_text, text = 0)
        name_col.set_expand(True)
        self.treeview.append_column(name_col)
        key_text = Gtk.CellRendererText()
        key_col = Gtk.TreeViewColumn("Key", key_text, text = 1)
        key_col.set_expand(True)
        self.treeview.append_column(key_col)
        format_text = Gtk.CellRendererText()
        format_col = Gtk.TreeViewColumn("Format", format_text, text = 2)
        format_col.set_expand(True)
        self.treeview.append_column(format_col)
        datec_text = Gtk.CellRendererText()
        datec_col = Gtk.TreeViewColumn("Date Created", datec_text, text = 3)
        datec_col.set_expand(True)
        self.treeview.append_column(datec_col)
        datee_text = Gtk.CellRendererText()
        datee_col = Gtk.TreeViewColumn("Date Expires", datee_text, text = 4)
        datee_col.set_expand(True)
        self.treeview.append_column(datee_col)
        expo_text = Gtk.CellRendererText()
        expo_col = Gtk.TreeViewColumn("Exposure", expo_text, text = 5)
        expo_col.set_expand(True)
        self.treeview.append_column(expo_col)
        size_text = Gtk.CellRendererText()
        size_col = Gtk.TreeViewColumn("Size", size_text, text = 6)
        size_col.set_expand(True)
        self.treeview.append_column(size_col)
        hits_text = Gtk.CellRendererText()
        hits_col = Gtk.TreeViewColumn("Hits", hits_text, text = 7)
        hits_col.set_expand(True)
        self.treeview.append_column(hits_col)
        url_text = Gtk.CellRendererText()
        url_col = Gtk.TreeViewColumn("URL", url_text, text = 8)
        url_col.set_expand(True)
        self.treeview.append_column(url_col)
        
        # Build the interface.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        scrolled_win.add(self.treeview)
        self.get_content_area().add(scrolled_win)
        
        # Add the data.
        for i in data:
            self.liststore.append(i)
        
        # Connect the treeview for double clicks.
        self.treeview.connect("row-activated", self.activate)
        
        # Show the dialog.
        self.show_all()
    
    
    def activate(self, treeiter, path, user_data):
        """Sends a click event to the button to load a paste."""
        
        self.get_btn.clicked()
