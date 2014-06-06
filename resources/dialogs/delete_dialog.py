# -*- coding: utf-8 -*-


# This file defines the Delete Paste dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class DeletePasteDialog(Gtk.Dialog):
    """Shows the delete paste dialog."""
    
    def __init__(self, parent, data):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Delete Paste", parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(500, 300)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
         # Create the ListStore for storing the data.
        self.liststore = Gtk.ListStore(str, str, str, str)
        
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
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
