# -*- coding: utf-8 -*-


# This file defines the recent paste list dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class ListRecentDialog(Gtk.Dialog):
    """Shows the list dialog."""
    def __init__(self, parent, title, data):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(1200, 500)
        self.get_btn = self.add_button("Get Paste", 9)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the columns for displaying the pastes.
        self.liststore = Gtk.ListStore(str, str, str, str, str)
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
        time_text = Gtk.CellRendererText()
        time_col = Gtk.TreeViewColumn("Time Created", time_text, text = 3)
        time_col.set_expand(True)
        self.treeview.append_column(time_col)
        link_text = Gtk.CellRendererText()
        link_col = Gtk.TreeViewColumn("URL", link_text, text = 4)
        link_col.set_expand(True)
        self.treeview.append_column(link_col)
        
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
