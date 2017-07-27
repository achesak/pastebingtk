# -*- coding: utf-8 -*-


# This file defines the user details dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class UserDetailsDialog(Gtk.Dialog):
    """Shows the user details dialog."""
    def __init__(self, parent, title, data):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(400, 300)
        if not title.startswith("Paste"):
            self.add_button("View Profile", 9)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the columns.
        self.liststore = Gtk.ListStore(str, str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        field_text = Gtk.CellRendererText()
        field_col = Gtk.TreeViewColumn("Field", field_text, text = 0)
        field_col.set_min_width(200)
        self.treeview.append_column(field_col)
        value_text = Gtk.CellRendererText()
        value_col = Gtk.TreeViewColumn("Value", value_text, text = 1)
        value_col.set_expand(True)
        self.treeview.append_column(value_col)
        
        # Build the interface.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        scrolled_win.add(self.treeview)
        self.get_content_area().add(scrolled_win)
        
        # Add the data.
        for i in data:
            self.liststore.append(i)
        
        # Show the dialog.
        self.show_all()
