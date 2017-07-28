# -*- coding: utf-8 -*-


# This file defines the Delete Paste dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class DeletePasteDialog(Gtk.Dialog):
    """Shows the delete paste dialog."""

    def __init__(self, parent, data):
        """Create the dialog."""

        # Create the dialog.
        Gtk.Dialog.__init__(self, "Delete Paste", parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(1000, 500)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Delete", Gtk.ResponseType.OK)

        # Create the columns for displaying the paste info.
        self.liststore = Gtk.ListStore(str, str, str, str)
        self.treeview = Gtk.TreeView(model=self.liststore)
        name_text = Gtk.CellRendererText()
        name_col = Gtk.TreeViewColumn("Name", name_text, text=0)
        name_col.set_expand(True)
        self.treeview.append_column(name_col)
        key_text = Gtk.CellRendererText()
        key_col = Gtk.TreeViewColumn("Key", key_text, text=1)
        key_col.set_expand(True)
        self.treeview.append_column(key_col)
        format_text = Gtk.CellRendererText()
        format_col = Gtk.TreeViewColumn("Format", format_text, text=2)
        format_col.set_expand(True)
        self.treeview.append_column(format_col)
        datec_text = Gtk.CellRendererText()
        datec_col = Gtk.TreeViewColumn("Date Created", datec_text, text=3)
        datec_col.set_expand(True)
        self.treeview.append_column(datec_col)

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
