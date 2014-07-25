# -*- coding: utf-8 -*-


# This file defines the user details dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class UserDetailsDialog(Gtk.Dialog):
    """Shows the user details dialog."""
    def __init__(self, parent, title, data):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(400, 300)
        
        # Add the buttons.
        self.add_button("Open Profile", 9)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        # Create the Field column.
        field_text = Gtk.CellRendererText()
        field_col = Gtk.TreeViewColumn("Field", field_text, text = 0)
        self.treeview.append_column(field_col)
        # Create the Value column.
        value_text = Gtk.CellRendererText()
        value_col = Gtk.TreeViewColumn("Value", value_text, text = 1)
        self.treeview.append_column(value_col)
        
        # Create the ScrolledWindow for displaying the list with a scrollbar.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        # Display the TreeView.
        scrolled_win.add(self.treeview)
        self.get_content_area().add(scrolled_win)
        
        # Add the data.
        for i in data:
            self.liststore.append(i)
        
        # Show the dialog. There's no need to get the response.
        self.show_all()
