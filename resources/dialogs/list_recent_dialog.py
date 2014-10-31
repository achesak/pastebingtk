# -*- coding: utf-8 -*-


# This file defines the recent paste list dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class ListRecentDialog(Gtk.Dialog):
    """Shows the list dialog."""
    def __init__(self, parent, title, data):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(950, 300)
        
        # Add the buttons.
        self.add_button("Get Paste", 9)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str, str, str, str)
        
        # Create the TreeView for displaying the data.
        self.treeview = Gtk.TreeView(model = self.liststore)
        # Create the Name column.
        name_text = Gtk.CellRendererText()
        name_col = Gtk.TreeViewColumn("Name", name_text, text = 0)
        self.treeview.append_column(name_col)
        # Create the Key column.
        key_text = Gtk.CellRendererText()
        key_col = Gtk.TreeViewColumn("Key", key_text, text = 1)
        self.treeview.append_column(key_col)
        # Create the Format column.
        format_text = Gtk.CellRendererText()
        format_col = Gtk.TreeViewColumn("Format", format_text, text = 2)
        self.treeview.append_column(format_col)
        # Create the Time Created column.
        time_text = Gtk.CellRendererText()
        time_col = Gtk.TreeViewColumn("Time Created", time_text, text = 3)
        self.treeview.append_column(time_col)
        # Create the Link column.
        link_text = Gtk.CellRendererText()
        link_col = Gtk.TreeViewColumn("Link", link_text, text = 4)
        self.treeview.append_column(link_col)
        
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
