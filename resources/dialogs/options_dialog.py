# -*- coding: utf-8 -*-


# This file defines the Add New dialog.


# Import GTK for the dialog.
from gi.repository import Gtk

# Import pastebin lists.
from resources.python_pastebin.pastebin_lists import *


class OptionsDialog(Gtk.Dialog):
    """Shows the "Options" dialog."""

    def __init__(self, parent, config):
        """Create the dialog."""

        # Create the dialog.
        Gtk.Dialog.__init__(self, "Options", parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)

        # Create the notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)

        # Create the General tab
        opt_box = self.get_content_area()
        gen_grid = Gtk.Grid()
        gen_grid.set_column_spacing(10)
        gen_grid.set_row_spacing(5)
        gen_grid_lbl = Gtk.Label("General")

        # Create the remember last username checkbox.
        self.user_chk = Gtk.CheckButton("Remember last username")
        self.user_chk.set_active(config["remember_username"])
        self.user_chk.set_tooltip_text("Remember and restore the last username after application is restarted")
        self.user_chk.set_margin_top(5)
        self.user_chk.set_margin_left(5)
        self.user_chk.set_margin_right(5)
        gen_grid.attach(self.user_chk, 0, 0, 2, 1)

        # Create the restore window size checkbox.
        self.win_chk = Gtk.CheckButton("Restore window size")
        self.win_chk.set_active(config["restore_window"])
        self.win_chk.set_tooltip_text("Remember and restore window size after application is restarted")
        self.win_chk.set_margin_left(5)
        self.win_chk.set_margin_right(5)
        gen_grid.attach_next_to(self.win_chk, self.user_chk, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the confirm on exit checkbox.
        self.exit_chk = Gtk.CheckButton("Confirm on exit")
        self.exit_chk.set_active(config["confirm_exit"])
        self.exit_chk.set_tooltip_text("Prompt for confirmation on application close")
        self.exit_chk.set_margin_left(5)
        self.exit_chk.set_margin_right(5)
        gen_grid.attach_next_to(self.exit_chk, self.win_chk, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the show line numbers checkbox.
        self.lin_chk = Gtk.CheckButton("Show line numbers")
        self.lin_chk.set_active(config["line_numbers"])
        self.lin_chk.set_tooltip_text("Show or hide line numbers in main editor")
        self.lin_chk.set_margin_left(5)
        self.lin_chk.set_margin_right(5)
        gen_grid.attach_next_to(self.lin_chk, self.exit_chk, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the check for spam filter checkbox.
        self.spam_chk = Gtk.CheckButton("Check for spam filter")
        self.spam_chk.set_active(config["check_spam"])
        self.spam_chk.set_tooltip_text(
            "Check if pastes get caught in the spam filter and provide an option to continue if they do")
        self.spam_chk.set_margin_left(5)
        self.spam_chk.set_margin_right(5)
        gen_grid.attach_next_to(self.spam_chk, self.lin_chk, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the pastes to retrieve label and spinbutton.
        lnum_lbl = Gtk.Label("Pastes to retrieve: ")
        lnum_lbl.set_tooltip_text("Number of trending, recent, and user-authored pastes to retrieve at once")
        lnum_lbl.set_alignment(0, 0.5)
        lnum_lbl.set_margin_left(5)
        lnum_lbl.set_margin_bottom(5)
        gen_grid.attach_next_to(lnum_lbl, self.spam_chk, Gtk.PositionType.BOTTOM, 1, 1)
        lnum_adj = Gtk.Adjustment(lower=1, upper=1000, step_increment=1)
        self.lnum_sbtn = Gtk.SpinButton(digits=0, adjustment=lnum_adj)
        self.lnum_sbtn.set_numeric(False)
        self.lnum_sbtn.set_value(config["pastes_retrieve"])
        self.lnum_sbtn.set_margin_right(5)
        self.lnum_sbtn.set_margin_bottom(5)
        gen_grid.attach_next_to(self.lnum_sbtn, lnum_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the Defaults tab.
        def_grid = Gtk.Grid()
        def_grid.set_column_spacing(10)
        def_grid.set_row_spacing(5)
        def_grid_lbl = Gtk.Label("Defaults")

        # Create the default name label and entry.
        name_lbl = Gtk.Label("Default name: ")
        name_lbl.set_tooltip_text("Default name to use when creating a paste")
        name_lbl.set_alignment(0, 0.5)
        name_lbl.set_margin_top(5)
        name_lbl.set_margin_left(5)
        def_grid.attach(name_lbl, 0, 0, 1, 1)
        self.name_ent = Gtk.Entry()
        self.name_ent.set_text(config["default_name"])
        self.name_ent.set_margin_top(5)
        self.name_ent.set_margin_right(5)
        def_grid.attach_next_to(self.name_ent, name_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the default format label and combobox.
        form_lbl = Gtk.Label("Default format: ")
        form_lbl.set_tooltip_text("Default format to use when creating a paste")
        form_lbl.set_alignment(0, 0.5)
        form_lbl.set_margin_left(5)
        def_grid.attach_next_to(form_lbl, name_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.form_com = Gtk.ComboBoxText()
        for i in FORMATS_LIST:
            self.form_com.append_text(i)
        self.form_com.set_active(FORMATS_LIST.index(config["default_format"]))
        self.form_com.set_margin_right(5)
        def_grid.attach_next_to(self.form_com, form_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the default expiration label and combobox.
        expi_lbl = Gtk.Label("Default expiration: ")
        expi_lbl.set_tooltip_text("Default expiration to use when creating a paste")
        expi_lbl.set_alignment(0, 0.5)
        expi_lbl.set_margin_left(5)
        def_grid.attach_next_to(expi_lbl, form_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expi_com = Gtk.ComboBoxText()
        for i in EXPIRE_LIST:
            self.expi_com.append_text(i)
        self.expi_com.set_active(EXPIRE_LIST.index(config["default_expiration"]))
        self.expi_com.set_margin_right(5)
        def_grid.attach_next_to(self.expi_com, expi_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the default exposure label and combobox.
        expo_lbl = Gtk.Label("Default exposure: ")
        expo_lbl.set_tooltip_text("Default exposure to use when creating a paste")
        expo_lbl.set_alignment(0, 0.5)
        expo_lbl.set_margin_left(5)
        expo_lbl.set_margin_bottom(5)
        def_grid.attach_next_to(expo_lbl, expi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expo_com = Gtk.ComboBoxText()
        for i in EXPOSURE_LIST:
            self.expo_com.append_text(i)
        self.expo_com.set_active(EXPOSURE_LIST.index(config["default_exposure"]))
        self.expo_com.set_margin_right(5)
        self.expo_com.set_margin_bottom(5)
        def_grid.attach_next_to(self.expo_com, expo_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the Technical tab.
        tech_grid = Gtk.Grid()
        tech_grid.set_column_spacing(10)
        tech_grid.set_row_spacing(5)
        tech_grid_lbl = Gtk.Label("Technical")

        # Create the developer key label and entry.
        devk_lbl = Gtk.Label("Developer key: ")
        devk_lbl.set_tooltip_text("Pastebin developer key, required to use Pastebin API")
        devk_lbl.set_alignment(0, 0.5)
        devk_lbl.set_margin_top(5)
        devk_lbl.set_margin_left(5)
        tech_grid.attach(devk_lbl, 0, 0, 1, 1)
        self.devk_ent = Gtk.Entry()
        self.devk_ent.set_text(config["dev_key"])
        self.devk_ent.set_margin_top(5)
        self.devk_ent.set_margin_right(5)
        tech_grid.attach_next_to(self.devk_ent, devk_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the developer key description label.
        devk_desc_lbl = Gtk.Label(
            "Please add your own developer key to\nprevent limits to the number of pastes that\ncan be created.\nThank you.")
        devk_desc_lbl.set_margin_left(5)
        devk_desc_lbl.set_margin_right(5)
        devk_desc_lbl.set_margin_bottom(5)
        tech_grid.attach_next_to(devk_desc_lbl, devk_lbl, Gtk.PositionType.BOTTOM, 2, 1)

        # Add the notebook.
        opt_box.add(notebook)
        notebook.append_page(gen_grid, gen_grid_lbl)
        notebook.append_page(def_grid, def_grid_lbl)
        notebook.append_page(tech_grid, tech_grid_lbl)

        # Show the dialog.
        self.show_all()
