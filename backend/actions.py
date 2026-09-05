# ============================================================
# NOVA — actions.py
# This file's only job: actually DO things on the computer.
# It knows how to open/close apps, open websites and folders,
# search the web, control volume, take screenshots, check the
# time/battery, and lock the computer.
# ============================================================

import os
import subprocess
import webbrowser
import ctypes
from urllib.parse import quote_plus
from datetime import datetime


# ============================================================
# Applications: open
# ============================================================

def open_chrome():
    """
    Attempts to open Google Chrome on Windows.
    If Chrome can't be started, this prints a friendly message
    instead of crashing the rest of Nova.
    """

    try:
        # "start chrome" is a Windows command that asks Windows
        # itself to launch Chrome, the same as typing it into
        # the Run box. shell=True is required because "start"
        # is a built-in command of the Windows command shell,
        # not a standalone program Python could run directly.
        subprocess.Popen("start chrome", shell=True)
        print("Nova: Opening Chrome...")

    except FileNotFoundError:
        print("Nova: I couldn't find the command to open Chrome.")

    except Exception as error:
        print(f"Nova: Something went wrong opening Chrome -> {error}")

def open_brave():
    try:
        brave_paths = [
            os.path.expandvars(r"%PROGRAMFILES%\BraveSoftware\Brave-Browser\Application\brave.exe"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\BraveSoftware\Brave-Browser\Application\brave.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
        ]

        for brave_path in brave_paths:
            if os.path.exists(brave_path):
                subprocess.Popen([brave_path])
                print("Nova: Opening Brave...")
                return

        print("Nova: I couldn't find Brave on this computer.")

    except Exception as error:
        print(f"Nova: Something went wrong opening Brave -> {error}")


def open_notepad():
    """
    Attempts to open Notepad on Windows. Notepad is a built-in
    Windows program, so we can launch it by name directly.
    """

    try:
        subprocess.Popen(["notepad"])
        print("Nova: Opening Notepad...")

    except FileNotFoundError:
        print("Nova: I couldn't find Notepad on this computer.")

    except Exception as error:
        print(f"Nova: Something went wrong opening Notepad -> {error}")


def open_calculator():
    """
    Attempts to open the Calculator app on Windows.
    """

    try:
        subprocess.Popen(["calc"])
        print("Nova: Opening Calculator...")

    except FileNotFoundError:
        print("Nova: I couldn't find Calculator on this computer.")

    except Exception as error:
        print(f"Nova: Something went wrong opening Calculator -> {error}")


def open_file_explorer():
    """
    Attempts to open File Explorer on Windows.
    """

    try:
        subprocess.Popen(["explorer"])
        print("Nova: Opening File Explorer...")

    except FileNotFoundError:
        print("Nova: I couldn't find File Explorer on this computer.")

    except Exception as error:
        print(f"Nova: Something went wrong opening File Explorer -> {error}")




# ============================================================
# Applications: close
# ============================================================

# Maps the simple name Nova understands to the actual Windows
# process name "taskkill" needs to find and stop it.
# Note: on some Windows versions the Calculator app's real
# process name can differ. If closing Calculator doesn't work
# on your machine, check its exact name in Task Manager's
# "Details" tab and update the entry below.
PROCESS_NAMES = {
    "chrome": "chrome.exe",
    "brave": "brave.exe",
    "notepad": "notepad.exe",
    "calculator": "CalculatorApp.exe",
}


def close_application(app_name):
    """
    Attempts to close a running application by asking Windows to
    end its process.

    "taskkill" is a command built into Windows (not a Python
    package) that can stop a running program by name. "/IM"
    specifies which program (by executable name), and "/F"
    forces it to close immediately.
    """

    try:
        process_name = PROCESS_NAMES.get(app_name)

        if process_name is None:
            print(f"Nova: I don't know how to close '{app_name}'.")
            return

        result = subprocess.run(
            ["taskkill", "/IM", process_name, "/F"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print(f"Nova: Closed {app_name}.")
        else:
            # A non-zero result usually just means the app
            # wasn't running in the first place.
            print(f"Nova: {app_name} doesn't seem to be running.")

    except Exception as error:
        print(f"Nova: Something went wrong closing {app_name} -> {error}")


# ============================================================
# Websites and web search
# ============================================================

def open_website(url):
    """
    Opens the given URL in the user's default web browser.

    "webbrowser" is part of Python's standard library, so no
    extra installation is needed. It doesn't launch a specific
    browser itself — it asks the operating system to open the
    URL with whatever browser is already set as default.
    """

    try:
        opened = webbrowser.open(url)

        if opened:
            print(f"Nova: Opening {url} in your browser...")
        else:
            print(f"Nova: I couldn't find a browser to open {url}.")

    except Exception as error:
        print(f"Nova: Something went wrong opening the website -> {error}")


def search_google(query):
    """
    Opens a Google search for the given query in the user's
    default web browser. The query is URL-encoded first, which
    converts spaces and special characters into a safe format
    for use inside a URL.
    """

    try:
        encoded_query = quote_plus(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"

        opened = webbrowser.open(search_url)

        if opened:
            print(f"Nova: Searching Google for '{query}'...")
        else:
            print(f"Nova: I couldn't find a browser to search for '{query}'.")

    except Exception as error:
        print(f"Nova: Something went wrong searching Google -> {error}")


def search_youtube(query):
    """
    Opens a YouTube search for the given query in the user's
    default web browser, the same way search_google() does for
    Google.
    """

    try:
        encoded_query = quote_plus(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"

        opened = webbrowser.open(search_url)

        if opened:
            print(f"Nova: Searching YouTube for '{query}'...")
        else:
            print(f"Nova: I couldn't find a browser to search for '{query}'.")

    except Exception as error:
        print(f"Nova: Something went wrong searching YouTube -> {error}")

def search_brave(query):
    """
    Opens a Brave search for the given query in the user's
    default web browser.
    """

    try:
        encoded_query = quote_plus(query)
        search_url = f"https://search.brave.com/search?q={encoded_query}"

        opened = webbrowser.open(search_url)

        if opened:
            print(f"Nova: Searching Brave for '{query}'...")
        else:
            print(f"Nova: I couldn't find a browser to search for '{query}'.")

    except Exception as error:
        print(f"Nova: Something went wrong searching Brave -> {error}")

# ============================================================
# Windows folders
# ============================================================

# Maps the simple name Nova understands to the folder's real
# name inside the user's home folder.
FOLDER_PATHS = {
    "downloads": "Downloads",
    "documents": "Documents",
    "desktop": "Desktop",
}


def open_folder(folder_name):
    """
    Opens one of the user's common Windows folders (Downloads,
    Documents, or Desktop) in File Explorer.

    os.path.expanduser("~") gives the path to the current
    user's home folder (e.g. C:\\Users\\YourName), and each of
    these folders sits directly inside it.
    """

    try:
        subfolder = FOLDER_PATHS.get(folder_name)

        if subfolder is None:
            print(f"Nova: I don't know a folder called '{folder_name}'.")
            return

        folder_path = os.path.join(os.path.expanduser("~"), subfolder)

        if not os.path.isdir(folder_path):
            print(f"Nova: I couldn't find the folder at {folder_path}.")
            return

        # os.startfile() is a Windows-only standard library
        # function that opens a file or folder with whatever
        # program Windows would normally use — for a folder,
        # that's File Explorer.
        os.startfile(folder_path)
        print(f"Nova: Opening {subfolder}...")

    except Exception as error:
        print(f"Nova: Something went wrong opening the folder -> {error}")


# ============================================================
# Volume control
# ============================================================

# Windows virtual key codes for the volume media keys — the
# same keys as the volume buttons on a keyboard.
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF


def _press_volume_key(vk_code, times=1):
    """
    Simulates pressing one of the keyboard's volume keys.

    keybd_event() is a function from Windows' own user32.dll
    that simulates a key press. We press the key (0 = key down)
    and then immediately release it (2 = KEYEVENTF_KEYUP),
    exactly like a quick tap on a real volume key. Pressing it
    a few times in a row makes the volume change noticeable,
    since each tap only moves it by a small step.
    """

    for _ in range(times):
        ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)  # key down
        ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)  # key up


def increase_volume():
    """Raises the system volume, like pressing Volume Up a few times."""

    try:
        _press_volume_key(VK_VOLUME_UP, times=3)
        print("Nova: Volume increased.")

    except Exception as error:
        print(f"Nova: Something went wrong changing the volume -> {error}")


def decrease_volume():
    """Lowers the system volume, like pressing Volume Down a few times."""

    try:
        _press_volume_key(VK_VOLUME_DOWN, times=3)
        print("Nova: Volume decreased.")

    except Exception as error:
        print(f"Nova: Something went wrong changing the volume -> {error}")


def mute_volume():
    """Toggles mute, like pressing the keyboard's Mute key."""

    try:
        _press_volume_key(VK_VOLUME_MUTE)
        print("Nova: Volume muted.")

    except Exception as error:
        print(f"Nova: Something went wrong muting the volume -> {error}")


# ============================================================
# Screenshot
# ============================================================

def take_screenshot():
    """
    Takes a screenshot of the whole screen and saves it to the
    user's Pictures/Screenshots folder (creating that folder if
    it doesn't exist yet). Returns the saved file path on
    success, or None if something went wrong.
    """

    # Pillow's ImageGrab is imported here, inside the function,
    # rather than at the top of the file. That way, if Pillow
    # isn't installed, only THIS feature fails when it's used —
    # the rest of Nova still works normally instead of the whole
    # program crashing on startup.
    try:
        from PIL import ImageGrab
    except ImportError:
        print("Nova: Screenshots need the 'Pillow' package. Install it with: pip install Pillow")
        return None

    try:
        screenshots_folder = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
        os.makedirs(screenshots_folder, exist_ok=True)  # create it if it doesn't exist

        # A timestamp in the filename means every screenshot
        # gets a unique name instead of overwriting the last one.
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"nova_screenshot_{timestamp}.png"
        filepath = os.path.join(screenshots_folder, filename)

        screenshot = ImageGrab.grab()
        screenshot.save(filepath)

        print(f"Nova: Screenshot saved to {filepath}")
        return filepath

    except Exception as error:
        print(f"Nova: Something went wrong taking the screenshot -> {error}")
        return None


# ============================================================
# System information
# ============================================================

def get_current_time():
    """
    Returns the current time as a friendly, spoken-style string
    like "3:45 PM".
    """

    now = datetime.now()
    # %I:%M %p gives something like "03:45 PM"; lstrip("0")
    # removes the leading zero so it reads more naturally.
    return now.strftime("%I:%M %p").lstrip("0")


def get_battery_level():
    """
    Returns the current battery percentage (0-100) as an
    integer, or None if this device has no battery (e.g. a
    desktop PC) or the battery status can't be read.

    Python's standard library doesn't expose battery
    information directly, so this uses the "psutil" package —
    a well-established, widely-used library for exactly this
    kind of system information.
    """

    try:
        import psutil
    except ImportError:
        print("Nova: Battery status needs the 'psutil' package. Install it with: pip install psutil")
        return None

    try:
        battery = psutil.sensors_battery()

        if battery is None:
            # No battery detected — likely a desktop computer.
            return None

        return round(battery.percent)

    except Exception as error:
        print(f"Nova: Something went wrong checking the battery -> {error}")
        return None


# ============================================================
# Lock computer
# ============================================================

def lock_computer():
    """
    Locks the computer immediately, showing the Windows lock
    screen — the same as pressing Windows key + L.

    ctypes lets Python call functions directly from Windows'
    own system libraries. LockWorkStation() is a function built
    into user32.dll, part of Windows itself, so no extra
    package is needed.
    """

    try:
        ctypes.windll.user32.LockWorkStation()
        print("Nova: Locking your computer...")

    except Exception as error:
        print(f"Nova: Something went wrong locking the computer -> {error}")