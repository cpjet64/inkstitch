# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import traceback
import sys
import platform
import subprocess
from glob import glob


class InkstitchException(Exception):
    pass


def _generic_os_version():
    system_name = platform.system() or "Unknown OS"
    release = platform.release()
    if release:
        return f"{system_name} {release}"
    return system_name


def _linux_os_version():
    # Getting linux version method used here is for systemd and nonsystemd linux.
    for release_file in glob("/etc/*-release"):
        try:
            with open(release_file, encoding="utf-8", errors="ignore") as release_data:
                for line in release_data:
                    if line.startswith("PRETTY_NAME="):
                        return line.split("=", 1)[1].strip().strip('"')
        except OSError:
            continue

    return _generic_os_version()


def get_os_version():
    if sys.platform == "win32":
        # To get the windows version, python functions are used
        # Using python subprocess with cmd.exe in windows is currently a security risk
        return "Windows " + platform.release() + " version: " + platform.version()
    elif sys.platform == "darwin":
        # macOS command line program provides more accurate info than python functions
        try:
            mac_v1 = subprocess.run(["sw_vers"], capture_output=True, text=True)
            mac_v1 = str(mac_v1.stdout.strip())
            mac_v2 = subprocess.run(["uname", "-m"], capture_output=True, text=True)
            mac_v2 = str(mac_v2.stdout.strip())
            return mac_v1 + "\nCPU:\t\t\t\t" + mac_v2
        except OSError:
            return _generic_os_version()
    elif sys.platform == "linux":
        return _linux_os_version()

    return _generic_os_version()


def format_uncaught_exception():
    """Format the current exception as a request for a bug report.

    Call this inside an except block so that there is an exception that we can
    call traceback.format_exc() on.
    """

    # importing locally to avoid any possibility of circular import
    from lib.utils import version
    from .i18n import _

    message = ""
    message += _("Ink/Stitch experienced an unexpected error. This means it is a bug in Ink/Stitch.")
    message += "\n\n"
    # L10N this message is followed by a URL: https://github.com/inkstitch/inkstitch/issues/new
    message += _("If you'd like to help please\n"
                 "- copy the entire error message below\n"
                 "- save your SVG file and\n"
                 "- create a new issue at")
    message += " https://github.com/inkstitch/inkstitch/issues/new\n\n"
    message += _("Include the error description and also (if possible) the svg file.")
    message += '\n\n'
    message += get_os_version()
    message += '\n\n'
    message += version.get_inkstitch_version() + '\n'
    message += traceback.format_exc()

    return message
