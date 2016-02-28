# -*- coding: utf-8 -*-


# This file defines the Get Paste dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class GetPasteDialog(Gtk.Dialog):
    """Shows the get paste dialog."""
    
    def __init__(self, parent):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, "Get Paste", parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        new_box.add(new_grid)
        
        # Create the name label and entry.
        key_lbl = Gtk.Label("Paste Key: ")
        key_lbl.set_alignment(0, 0.5)
        new_grid.add(key_lbl)
        self.key_ent = Gtk.Entry()
        new_grid.attach_next_to(self.key_ent, key_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog.
        self.show_all()
