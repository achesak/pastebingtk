# -*- coding: utf-8 -*-


# This file defines the Create Paste dialog.


# Import GTK for the dialog.
from gi.repository import Gtk

# Import application modules
from resources.python_pastebin.pastebin_lists import FORMATS_LIST, EXPIRE_LIST, EXPOSURE_LIST


class CreatePasteDialog(Gtk.Dialog):
    """Shows the new paste dialog."""
    
    def __init__(self, parent):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, "Create Paste", parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
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
        for i in EXPOSURE_LIST:
            self.form_com.append_text(i)
        self.form_com.set_active(0)
        new_grid.attach_next_to(self.form_com, form_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the expiration label and combobox.
        expi_lbl = Gtk.Label("Expiration: ")
        expi_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(expi_lbl, form_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expi_com = Gtk.ComboBoxText()
        for i in EXPIRE_LIST:
            self.expi_com.append_text(i)
        self.expi_com.set_active(0)
        new_grid.attach_next_to(self.expi_com, expi_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the exposure label and combobox.
        expo_lbl = Gtk.Label("Exposure: ")
        expo_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(expo_lbl, expi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expo_com = Gtk.ComboBoxText()
        for i in EXPOSURE_LIST:
            self.expo_com.append_text(i)
        self.expo_com.set_active(0)
        new_grid.attach_next_to(self.expo_com, expo_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Connect 'Enter' key to the OK button.
        self.name_ent.set_activates_default(True)
        ok_btn = self.get_widget_for_response(response_id = Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
