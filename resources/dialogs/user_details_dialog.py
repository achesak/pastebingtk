# -*- coding: utf-8 -*-


# This file defines the user details dialog.


# Import GTK for the dialog.
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gio

# Import python modules.
import urllib2

# Import application modules.
from resources.constants import *
from resources.python_pastebin.pastebin_dicts import *


class UserDetailsDialog(Gtk.Dialog):
    """Shows the user details dialog."""

    def __init__(self, parent, title, info, extra_info):
        """Create the dialog."""

        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(500, -1)
        self.add_button("View Profile", DialogResponse.VIEW_PROFILE)

        # Create the avatar image.
        dlg_box = self.get_content_area()
        avatar_img = Gtk.Image()
        try:
            response = urllib2.urlopen(info["avatar_url"])
            input_stream = Gio.MemoryInputStream.new_from_data(response.read(), None)
            pixbuf = Pixbuf.new_from_stream(input_stream, None)
            avatar_img.set_from_pixbuf(pixbuf)
        except urllib2.URLError:
            pass
        avatar_img.props.halign = Gtk.Align.CENTER
        avatar_img.set_hexpand(True)
        dlg_box.add(avatar_img)

        # Create the labels.
        name_lbl = Gtk.Label()
        name_lbl.set_markup("<span size=\"xx-large\"><a href=\"https://pastebin.com/u/" + info["name"] + "\">" + info["name"] + "</a></span>")
        name_lbl.set_margin_top(10)
        dlg_box.add(name_lbl)
        account_lbl = Gtk.Label()
        account_lbl.set_markup("<span size=\"medium\">" + ACCOUNT_TYPE[info["account_type"]] + " account</span>")
        account_lbl.set_margin_top(5)
        dlg_box.add(account_lbl)
        if len(extra_info) > 0:
            join_lbl = Gtk.Label()
            join_lbl.set_markup("<span size=\"medium\">Joined " + " ".join(extra_info[2][1].split(" ")[0:5]) + "</span>")
            join_lbl.set_margin_top(5)
            dlg_box.add(join_lbl)
        email_lbl = Gtk.Label()
        email_lbl.set_markup("<span size=\"medium\"><a href=\"mailto:" + info["email"] + "\">" + info["email"] + "</a></span>")
        email_lbl.set_margin_top(10)
        dlg_box.add(email_lbl)
        website_lbl = Gtk.Label()
        if info["website"]:
            website_lbl.set_markup("<span size=\"medium\"><a href=\"" + info["website"] + "\">" + info["website"] + "</a></span>")
        else:
            website_lbl.set_markup("<span size=\"medium\">No website provided</span>")
        website_lbl.set_margin_top(5)
        dlg_box.add(website_lbl)
        location_lbl = Gtk.Label()
        if info["location"]:
            location_lbl.set_markup("<span size=\"medium\">Located at " + info["location"] + "</span>")
        else:
            location_lbl.set_markup("<span size=\"medium\">No location provided</span>")
        location_lbl.set_margin_top(5)
        dlg_box.add(location_lbl)
        if len(extra_info) > 0:
            profile_view_lbl = Gtk.Label()
            profile_view_lbl.set_markup("<span size=\"medium\">" + extra_info[0][1] + " profile views</span>")
            profile_view_lbl.set_margin_top(10)
            dlg_box.add(profile_view_lbl)
            paste_view_lbl = Gtk.Label()
            paste_view_lbl.set_markup("<span size=\"medium\">" + extra_info[1][1] + " total paste views</span>")
            paste_view_lbl.set_margin_top(5)
            dlg_box.add(paste_view_lbl)

        # Show the dialog.
        self.show_all()
