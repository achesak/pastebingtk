# -*- coding: utf-8 -*-


################################################################################
#
# PastebinGTK: io.py
# This module reads and writes data and application files
#
################################################################################


# Import json for saving and loading the configuration and application files.
import json


def save_file(filename, data):
    """Generic function for saving a file."""
    
    try:
        data_file = open(filename, "w")
        data_file.write(data)
        data_file.close()
        
    except IOError as e:
        print("save_file(): Error writing to file (IOError):\n%s" % e)


def read_file(filename):
    """Generic function for reading from a file."""
    
    try:
        data_file = open(filename, "r")
        data = data_file.read()
        data_file.close()
        
    except IOError as e:
        print("read_file(): Error reading from file (IOError):\n%s" % e)
        data = ""
    
    return data


def save_application_data(main_dir, config, width, height, username):
    """Saves the application data."""

    application_data = {
        "width": width if config["restore_window"] else 700,
        "height": height if config["restore_window"] else 500,
        "username": username if config["remember_username"] else ""
    }
    
    try:
        app_file = open("%s/application_data.json" % main_dir, "w")
        json.dump(application_data, app_file)
        app_file.close()
    
    except IOError as e:
        print("save_application_data(): Error saving application data (IOError):\n%s" % e)

    except (TypeError, ValueError) as e:
        print("save_application_data(): Error saving application data (TypeError or ValueError):\n%s" % e)


def save_config(main_dir, config):
    """Saves the configuration."""
    
    try:
        config_file = open("%s/config" % main_dir, "w")
        json.dump(config, config_file)
        config_file.close()
        
    except IOError as e:
        print("save_config(): Error saving configuration file (IOError):\n%s" % e)
    
    except (TypeError, ValueError) as e:
        print("save_config(): Error saving configuration file (TypeError or ValueError):\n%s" % e)


def get_config(main_dir):
    """Gets the configuration."""
    
    try:
        default_config_file = open("resources/appdata/default_config.json", "r")
        default_config = json.load(default_config_file)
        default_config_file.close()
    
    except IOError as e:
        print("get_config(): Error reading default config file (IOError):\n%s" % e)
        sys.exit()
    
    except (TypeError, ValueError) as e:
        print("get_config(): Error reading default config file (TypeError or ValueError):\n%s" % e)
        sys.exit()

    config = default_config

    try:
        config_file = open("%s/config" % main_dir, "r")
        config = json.load(config_file)
        config_file.close()
    
    except IOError as e:
        print("get_config(): Error reading config file (IOError):\n%sContinuing with default..." % e)

    except (TypeError, ValueError) as e:
        print("get_config(): Error reading config file (TypeError or ValueError):\n%sContinuing with default..." % e)
    
    return config


def get_application_data(main_dir):
    """Gets the application data."""

    application_data = {
        "width": 700,
        "height": 500,
        "username": ""
    }

    try:
        app_file = open("%s/application_data.json" % main_dir, "r")
        application_data = json.load(app_file)
        app_file.close()

    except IOError as e:
        print("get_application_data(): Error reading application data file (IOError):\n%sContinuing with default..." % e)

    except (TypeError, ValueError) as e:
        print("get_application_data(): Error reading application data file (TypeError or ValueError):\n%sContinuing with default..." % e)

    return application_data


def get_ui_data():
    """Gets the UI data."""

    try:
        ui_file = open("resources/appdata/ui_data.json", "r")
        ui_data = json.load(ui_file)
        ui_file.close()

    except IOError as e:
        print("get_ui_data(): Error reading UI data file (IOError):\n%s" % e)
        sys.exit()

    except (TypeError, ValueError) as e:
        print("get_ui_data(): Error reading UI data file (TypeError or ValueError):\n%s" % e)
        sys.exit()

    return ui_data


def get_menu_data():
    """Gets the menu data."""

    try:
        menu_file = open("resources/appdata/menu.xml")
        menu_data = menu_file.read()
        menu_file.close()

    except IOError as e:
        print("get_menu_data(): Error reading menu data file (IOError):\n%s" % e)
        sys.exit()

    except (TypeError, ValueError)as e:
        print("get_menu_data(): Error reading menu data file (TypeError or ValueError):\n%s" % e)
        sys.exit()

    return menu_data