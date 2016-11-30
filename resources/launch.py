# -*- coding: utf-8 -*-


################################################################################
#
# PastebinGTK: launch.py
# This module sets up the application on launch.
#
################################################################################



# Import os and platform for path manipulation.
import os
import platform


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
