# -*- coding: utf-8 -*-


# This file defines the functions for reading and writing data.


# Import json for saving the configuration file.
import json


def save_file(filename, data):
    """Generic function for saving a file."""
    
    try:
        data_file = open(filename, "w")
        data_file.write(data)
        data_file.close()
        
    except IOError:
        print("Error writing to file (IOError).")


def read_file(filename):
    """Generic function for reading from a file."""
    
    # Read the data.
    try:
        data_file = open(filename, "r")
        data = data_file.read()
        data_file.close()
        
    except IOError:
        print("Error reading from file (IOError).")
    
    return data


def save_window_size(main_dir, height, width):
    """Saves the window size."""
    
    try:
        wins_file = open("%s/window_size" % main_dir, "w")
        wins_file.write("%d\n%d" % (height, width))
        wins_file.close()
    
    except IOError:
        print("Error saving window size file (IOError).")


def save_config(main_dir, config):
    """Saves the configuration."""
    
    try:
        config_file = open("%s/config" % main_dir, "w")
        json.dump(config, config_file)
        config_file.close()
        
    except IOError:
        print("Error saving configuration file (IOError).")
    
    except (TypeError, ValueError):
        print("Error saving configuration file (TypeError or ValueError).")


def save_username(main_dir, config, username):
    """Saves the username of the logged in user."""
    
    if config["remember_username"]:
            
        try:
            user_file = open("%s/username" % main_dir, "w")
            user_file.write(username)
            user_file.close()
        
        except IOError:
            print("Error saving username file (IOError).")
