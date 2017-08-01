# -*- coding: utf-8 -*-


# This file defines the paste details dialog.


# Import GTK for the dialog.
from gi.repository import Gtk

# Import application modules
from resources.constants import *


class PasteDetailsDialog(Gtk.Dialog):
    """Shows the paste details dialog."""

    def __init__(self, parent, title, name, username, url, views, created, expires):
        """Create the dialog."""

        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(500, -1)
        self.add_button("View Paste", DialogResponse.VIEW_PASTE)
        self.add_button("Close", Gtk.ResponseType.CLOSE)

        # Create the labels.
        dlg_box = self.get_content_area()
        name_lbl = Gtk.Label()
        name_lbl.set_markup("<span size=\"xx-large\"><a href=\"" + url + "\">" + name + "</a></span>")
        name_lbl.set_margin_top(5)
        dlg_box.add(name_lbl)
        user_lbl = Gtk.Label()
        user_lbl.set_markup("<span size=\"large\">Uploaded by <b>" + username + "</b></span>")
        user_lbl.set_margin_top(5)
        dlg_box.add(user_lbl)
        view_lbl = Gtk.Label()
        view_lbl.set_markup("<span size=\"medium\">" + views + " view%s</span>" % "s" if int(views) != 1 else "")
        view_lbl.set_margin_top(15)
        dlg_box.add(view_lbl)
        create_lbl = Gtk.Label()
        create_lbl.set_markup("<span size=\"medium\">Created on " + created + "</span>")
        create_lbl.set_margin_top(15)
        dlg_box.add(create_lbl)
        expire_lbl = Gtk.Label()
        if expires == "Never":
            expire_lbl.set_markup("<span size=\"medium\">Expires never</span>")
        else:
            expire_lbl.set_markup("<span size=\"medium\">Expires in " + expires.lower() + "</span>")
        expire_lbl.set_margin_top(5)
        expire_lbl.set_margin_bottom(5)
        dlg_box.add(expire_lbl)

        # Show the dialog.
        self.show_all()
