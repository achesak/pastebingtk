# -*- coding: utf-8 -*-


# This file defines the paste list view dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class ListPastesDialog(Gtk.Dialog):
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
        self.liststore = Gtk.ListStore(str, str, str, str, str, str, str, str, str)
        
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
        # Create the Date Created column.
        datec_text = Gtk.CellRendererText()
        datec_col = Gtk.TreeViewColumn("Date Created", datec_text, text = 3)
        self.treeview.append_column(datec_col)
        # Create the Date Expires column.
        datee_text = Gtk.CellRendererText()
        datee_col = Gtk.TreeViewColumn("Date Expires", datee_text, text = 4)
        self.treeview.append_column(datee_col)
        # Create the Exposure column.
        expo_text = Gtk.CellRendererText()
        expo_col = Gtk.TreeViewColumn("Exposure", expo_text, text = 5)
        self.treeview.append_column(expo_col)
        # Create the Size column.
        size_text = Gtk.CellRendererText()
        size_col = Gtk.TreeViewColumn("Size", size_text, text = 6)
        self.treeview.append_column(size_col)
        # Create the Hits column.
        hits_text = Gtk.CellRendererText()
        hits_col = Gtk.TreeViewColumn("Hits", hits_text, text = 7)
        self.treeview.append_column(hits_col)
        # Create the URL column.
        url_text = Gtk.CellRendererText()
        url_col = Gtk.TreeViewColumn("URL", url_text, text = 8)
        self.treeview.append_column(url_col)
        
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
