# -*- coding: utf-8 -*-


# This file defines variables used by the UI.


# Define the version and the title.
TITLE = "PastebinGTK"
VERSION = "0.1"

# Define the menu XML.
MENU_DATA = """
<ui>
  <menubar name="menubar">
    <menu action="pastebin_menu">
      <menuitem action="create_paste" />
      <menuitem action="get_paste" />
      <menuitem action="delete_paste" />
      <separator />
      <menuitem action="list_trending_pastes" />
      <menuitem action="list_users_pastes" />
      <separator />
      <menuitem action="login" />
      <menuitem action="logout" />
      <menuitem action="get_user_info" />
      <separator />
      <menuitem action="save" />
      <menuitem action="open" />
      <separator />
      <menuitem action="quit" />
    </menu>
    <menu action="options_menu">
      <menuitem action="options" />
    </menu>
    <menu action="help_menu">
      <menuitem action="about" />
      <separator />
      <menuitem action="help" />
    </menu>
  </menubar>
  <toolbar name="toolbar">
    <toolitem action="create_paste" />
    <toolitem action="get_paste" />
    <separator />
    <toolitem action="save" />
    <toolitem action="open" />
  </toolbar>
</ui>
"""
