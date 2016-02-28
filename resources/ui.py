# -*- coding: utf-8 -*-


# This file defines variables used by the UI.


# Define the application variables.
TITLE = "PastebinGTK"
VERSION = "1.3"
ICON_PATH = "resources/images/icon.png"

# Define the menu XML.
MENU_DATA = """
<ui>
  <menubar name="menubar">
    <menu action="pastebin_menu">
      <menuitem action="create_paste" />
      <menuitem action="get_paste" />
      <menuitem action="delete_paste" />
      <separator />
      <menuitem action="get_paste_info" />
      <separator />
      <menuitem action="list_trending_pastes" />
      <menuitem action="list_users_pastes" />
      <menuitem action="list_recent_pastes" />
      <separator />
      <menuitem action="quit" />
    </menu>
    <menu action="user_menu">
      <menuitem action="login" />
      <menuitem action="logout" />
      <separator />
      <menuitem action="user_details" />
    </menu>
    <menu action="text_menu">
      <menuitem action="save" />
      <menuitem action="open" />
    </menu>
    <menu action="options_menu">
      <menuitem action="options" />
    </menu>
    <menu action="help_menu">
      <menuitem action="about" />
    </menu>
  </menubar>
  <toolbar name="toolbar">
    <toolitem action="create_paste" />
    <toolitem action="get_paste" />
    <toolitem action="delete_paste" />
    <separator />
    <toolitem action="save" />
    <toolitem action="open" />
  </toolbar>
</ui>
"""
