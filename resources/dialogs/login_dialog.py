# -*- coding: utf-8 -*-


# This file defines the Login dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class LoginDialog(Gtk.Dialog):
    """Shows the login dialog."""
    
    def __init__(self, parent):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, "Login", parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        self.add_button("Skip", Gtk.ResponseType.CANCEL)
        self.add_button("Login", Gtk.ResponseType.OK)
        
        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
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
        
        # Show the dialog.
        self.show_all()
