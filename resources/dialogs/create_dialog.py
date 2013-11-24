# -*- coding: utf-8 -*-


# This file defines the Create Paste dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class CreatePasteDialog(Gtk.Dialog):
    """Shows the new paste dialog."""
    
    def __init__(self, parent):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Create Paste", parent, Gtk.DialogFlags.MODAL)
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
        
        # Create the name label and entry.
        name_lbl = Gtk.Label("Name: ")
        name_lbl.set_alignment(0, 0.5)
        new_grid.add(name_lbl)
        self.name_ent = Gtk.Entry()
        new_grid.attach_next_to(self.name_ent, name_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the format label and combobox.
        form_lbl = Gtk.Label("Format: ")
        form_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(form_lbl, name_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.form_com = Gtk.ComboBoxText()
        for i in ["None"]: ## FILL THIS!!!
            self.form_com.append_text(i)
        self.form_com.set_active(0)
        new_grid.attach_next_to(self.form_com, form_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the expiration label and combobox.
        expi_lbl = Gtk.Label("Expiration: ")
        expi_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(expi_lbl, form_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expi_com = Gtk.ComboBoxText()
        for i in ["Never", "10 Minutes", "1 Hour", "1 Day", "1 Week", "2 Weeks", "1 Month"]:
            self.expi_com.append_text(i)
        self.expi_com.set_active(0)
        new_grid.attach_next_to(self.expi_com, expi_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the exposure label and combobox.
        expo_lbl = Gtk.Label("Exposure: ")
        expo_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(expo_lbl, expi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expo_com = Gtk.ComboBoxText()
        for i in ["Public", "Unlisted", "Private"]:
            self.expo_com.append_text(i)
        self.expo_com.set_active(0)
        new_grid.attach_next_to(self.expo_com, expo_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
