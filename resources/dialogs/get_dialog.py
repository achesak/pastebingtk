# -*- coding: utf-8 -*-


# This file defines the Get Paste dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class GetPasteDialog(Gtk.Dialog):
    """Shows the get paste dialog."""

    def __init__(self, parent, title="Get Paste"):
        """Create the dialog."""

        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_size_request(400, -1)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)

        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        new_grid.set_column_spacing(3)
        new_grid.set_row_spacing(3)
        new_box.add(new_grid)

        # Create the paste exposure frame and radiobuttons.
        expo_frame = Gtk.Frame()
        expo_frame.set_label("Paste exposure")
        expo_grid = Gtk.Grid()
        expo_grid.set_column_spacing(5)
        expo_grid.set_row_spacing(5)
        expo_frame.add(expo_grid)
        self.public_rbtn = Gtk.RadioButton.new_with_label_from_widget(None, "Public or unlisted")
        self.private_rbtn = Gtk.RadioButton.new_with_label_from_widget(self.public_rbtn, "Private")
        expo_grid.add(self.public_rbtn)
        expo_grid.attach_next_to(self.private_rbtn, self.public_rbtn, Gtk.PositionType.BOTTOM, 1, 1)
        new_grid.add(expo_frame)

        # Create the key frame and entry,
        key_frame = Gtk.Frame()
        key_frame.set_label("Paste key")
        self.key_ent = Gtk.Entry()
        self.key_ent.set_hexpand(True)
        self.key_ent.grab_focus()
        key_frame.add(self.key_ent)
        new_grid.attach_next_to(key_frame, expo_frame, Gtk.PositionType.BOTTOM, 1, 1)

        # Connect 'Enter' key to the OK button.
        self.key_ent.set_activates_default(True)
        ok_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()

        # Show the dialog.
        self.show_all()
