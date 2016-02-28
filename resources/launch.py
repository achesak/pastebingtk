# -*- coding: utf-8 -*-


# This file defines the functions for launching and setting up the application.


# Import os for various things.
import os
# Import platform for getting the user's OS.
import platform
# Import json for loading and saving the configuration file.
import json


def get_main_dir():
    """Gets the location of the main directory."""
    
    # Get the path.
    if platform.system().lower() == "windows":
        main_dir = "C:\\.pastebingtk"
    else:
        main_dir = "%s/.pastebingtk" % os.path.expanduser("~")

    # Check to see if the directory exists, and create it if it doesn't.
    if not os.path.exists(main_dir) or not os.path.isdir(main_dir):
        os.makedirs(main_dir)
    
    return main_dir


def get_config(main_dir):
    """Gets the configuration."""
    
    try:
        config_file = open("%s/config" % main_dir, "r")
        config = json.load(config_file)
        config_file.close()
    
    except (IOError, ValueError):
        config = {"dev_key": "d2314ff616133e54f728918b8af1500e",
                  "prompt_login": True,
                  "remember_username": True,
                  "restore_window": True,
                  "confirm_exit": False,
                  "default_name": "",
                  "default_format": "None",
                  "default_expiration": "Never",
                  "default_exposure": "Public",
                  "line_numbers": True,
                  "syntax_highlight": True,
                  "syntax_guess": True,
                  "syntax_default": "",
                  "check_spam": True,
                  "pastes_retrieve": 50}
    
    return config


def get_last_username(main_dir, config):
    """Gets the username of the last logged on user."""
    
    username = ""
    if config["remember_username"]:
        
        try:
            user_file = open("%s/username" % main_dir, "r")
            username = user_file.read()
            user_file.close()
        
        except IOError:
            pass
    
    return username


def get_window_size(main_dir, config):
    """Gets the last window size."""
    
    try:
        wins_file = open("%s/window_size" % main_dir, "r")
        last_width = int(wins_file.readline())
        last_height = int(wins_file.readline())
        wins_file.close()
    
    except IOError:
        last_width = 700
        last_height = 500
    
    # If the user doesn't want to restore the window size, set the size to the default.
    if not config["restore_window"]:
        last_width = 700
        last_height = 500
    
    return last_width, last_height
    
