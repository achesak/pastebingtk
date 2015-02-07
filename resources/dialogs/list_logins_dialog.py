# -*- coding: utf-8 -*-


# This file defines the list logins dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class ListLoginsDialog(Gtk.Dialog):
    """Shows the list dialog."""
    def __init__(self, parent, title, data):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(500, 300)
        
        # Add the buttons.
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str, str)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        # Create the Date column.
        date_text = Gtk.CellRendererText()
        date_col = Gtk.TreeViewColumn("Date", date_text, text = 0)
        self.treeview.append_column(date_col)
        # Create the IP Address column.
        ip_text = Gtk.CellRendererText()
        ip_col = Gtk.TreeViewColumn("IP Address", ip_text, text = 1)
        self.treeview.append_column(ip_col)
        # Create the Type column.
        type_text = Gtk.CellRendererText()
        type_col = Gtk.TreeViewColumn("Type", type_text, text = 2)
        self.treeview.append_column(type_col)
        
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
