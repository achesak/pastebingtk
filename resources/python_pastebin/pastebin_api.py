# -*- coding: utf-8 -*-

# python-pastebin
# Wrapper of the pastebin.com API for the Python language.
# Released under the MIT open source license.

# This file works with the pastebin.com API, and allows for the creation,
# deletion, and listing of pastes.


# Import urlopen and urlencode.
# Try both for Python 2 and Python 3 compatability.
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
    from urllib import urlencode
# Import ElementTree for parsing XML.
import xml.etree.ElementTree as ElementTree


def create_user_key(devkey, username, password):
    """Gets a user session key."""
    
    params = {"api_dev_key": devkey,
              "api_user_name": username,
              "api_user_password": password}
    params = urlencode(params)
    
    response = urlopen("http://pastebin.com/api/api_login.php", params)
    data = response.read()
    response.close()
    
    return data


def create_paste(devkey, data, name = "", format_ = "", private = 0, expire = "", userkey = ""):
    """Creates a new paste."""
    
    params = {"api_option": "paste",
              "api_dev_key": devkey,
              "api_paste_code": data,
              "api_paste_name": name,
              "api_paste_private": str(private)}
    if format_:
        params["api_paste_format"] = format_
    if expire:
        params["api_paste_expire_date"] = expire
    if userkey:
        params["api_user_key"] = userkey
    params = urlencode(params)
    
    response = urlopen("http://pastebin.com/api/api_post.php", params)
    data = response.read()
    response.close()
    
    return data


def delete_paste(devkey, userkey, pastekey):
    """Deletes a paste."""
    
    params = {"api_option": "delete",
              "api_dev_key": devkey,
              "api_user_key": userkey,
              "api_paste_key": pastekey}
    params = urlencode(params)
    
    response = urlopen("http://pastebin.com/api/api_post.php", params)
    data = response.read()
    response.close()
    
    return data


def get_paste(pastekey):
    """Gets a paste."""
    
    response = urlopen("http://pastebin.com/raw.php?i=" + pastekey)
    data = response.read()
    response.close()
    
    return data


def list_users_pastes(devkey, userkey, results_limit = 50):
    """Gets a list of a user's pastes."""
    
    params = {"api_option": "list",
              "api_dev_key": devkey,
              "api_user_key": userkey,
              "api_results_limit": str(results_limit)}
    params = urlencode(params)
    
    response = urlopen("http://pastebin.com/api/api_post.php", params)
    data = "<pastebin>" + response.read() + "</pastebin>"
    response.close()
    
    pastes = []
    root = ElementTree.fromstring(data)
    
    for e in root:
        paste = {
            "key": e.find("paste_key").text,
            "date": e.find("paste_date").text,
            "title": e.find("paste_title").text,
            "size": e.find("paste_size").text,
            "expire_date": e.find("paste_expire_date").text,
            "private": e.find("paste_private").text,
            "format_long": e.find("paste_format_long").text,
            "format_short": e.find("paste_format_short").text,
            "url": e.find("paste_url").text,
            "hits": e.find("paste_hits").text
        }
        pastes.append(paste)
    
    return pastes


def list_trending_pastes(devkey):
    """Gets a list of a user's pastes."""
    
    params = {"api_option": "trends",
              "api_dev_key": devkey}
    params = urlencode(params)
    
    response = urlopen("http://pastebin.com/api/api_post.php", params)
    data = "<pastebin>" + response.read() + "</pastebin>"
    response.close()
    
    pastes = []
    root = ElementTree.fromstring(data)
    
    for e in root:
        paste = {
            "key": e.find("paste_key").text,
            "date": e.find("paste_date").text,
            "title": e.find("paste_title").text,
            "size": e.find("paste_size").text,
            "expire_date": e.find("paste_expire_date").text,
            "private": e.find("paste_private").text,
            "url": e.find("paste_url").text,
            "hits": e.find("paste_hits").text
        }
        pastes.append(paste)
    
    return pastes


def get_user_info(devkey, userkey):
    """Gets info about a user."""
    
    params = {"api_option": "userdetails",
              "api_dev_key": devkey,
              "api_user_key": userkey}
    params = urlencode(params)
    
    response = urlopen("http://pastebin.com/api/api_post.php", params)
    data = response.read()
    response.close()
    
    root = ElementTree.fromstring(data)
    info = {
        "name": root.find("user_name").text,
        "avatar_url": root.find("user_avatar_url").text,
        "account_type": root.find("user_account_type").text
    }
    if root.find("user_format_short"):
        info["format_short"] = root.find("user_format_short").text
    if root.find("user_expiration"):
        info["expiration"] = root.find("user_expiration").text
    if root.find("user_private"):
        info["private"] = root.find("private").text
    if root.find("user_website"):
        info["website"] = root.find("user_website").text
    if root.find("user_email"):
        info["email"] = root.find("user_email").text
    if root.find("user_location"):
        info["location"] = root.find("user_location").text
    
    return info
