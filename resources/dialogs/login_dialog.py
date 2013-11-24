# -*- coding: utf-8 -*-


# This file defines the Add Fossil dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class LoginDialog(Gtk.Dialog):
    """Shows the login dialog."""
    
    def __init__(self, parent):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Login", parent, Gtk.DialogFlags.MODAL)
        # Don't allow the user to resize the window.
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        new_box.add(new_grid)
        
        # Create the username label and entry.
        name_lbl = Gtk.Label("Username: ")
        name_lbl.set_alignment(0, 0.5)
        new_grid.add(name_lbl)
        self.name_ent = Gtk.Entry()
        new_grid.attach_next_to(self.name_ent, name_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the password label and entry.
        pass_lbl = Gtk.Label("Password: ")
        pass_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(pass_lbl, name_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.pass_ent = Gtk.Entry()
        self.pass_ent.set_visibility(False)
        new_grid.attach_next_to(self.pass_ent, pass_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
