# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.


# This module intentionally keeps only implementation details.
# Canonical debugger/profiler setup and developer workflows live in DEVELOPERS.md.
# Runtime options are configured through DEBUG_template.toml / DEBUG.toml and
# LOGGING_template.toml / LOGGING.toml.

# We have some ignores so you don't see errors if you don't have one or more of the debugger libraries installed.
# But in turn those ignores will cause unused-ignore errors if those libraries aren't installed...
# mypy: disable-error-code="unused-ignore"

import os
import sys

import socket  # to check if debugger is running

from .utils import safe_get  # mimic get method of dict with default value

import logging

logger = logging.getLogger("inkstitch")


# we intentionally disable flakes C901 - function is too complex, beacuse it is used only for debugging
# currently complexity is set 10 see 'make style', this means that function can have max 10 nested blocks, here we have more
# flake8: noqa: C901
def init_debugger(debug_type: str, ini: dict):
    if debug_type == "none":
        return

    debugger = debug_type

    try:
        if debugger == "vscode":
            import debugpy  # type: ignore[import-untyped, import-not-found]
        elif debugger == "pycharm":
            import pydevd_pycharm  # type: ignore[import-untyped, import-not-found]
        elif debugger == "pydev":
            import pydevd  # type: ignore[import-untyped, import-not-found]
        elif debugger == "file":
            pass
        else:
            raise ValueError(f"unknown debugger: '{debugger}'")

    except ImportError:
        logger.info(f"importing debugger failed (debugger disabled) for {debugger}")

    # pydevd likes to shout about errors to stderr whether I want it to or not
    with open(os.devnull, "w") as devnull:
        stderr = sys.stderr
        sys.stderr = devnull

        try:
            if debugger == "vscode":
                debugpy.connect(("localhost", 5678))
                debugpy.breakpoint()
            elif debugger == "pycharm":
                pydevd_pycharm.settrace("localhost", port=5678, stdoutToServer=True, stderrToServer=True)
            elif debugger == "pydev":
                pydevd.settrace()
            elif debugger == "file":
                pass
            else:
                raise ValueError(f"unknown debugger: '{debugger}'")

        except socket.error as error:
            logger.info(f"Debugging: connection to {debugger} failed: %s", error)
            logger.info(f"Be sure to run 'Start debugging server' in {debugger} to enable debugging.")
        else:
            logger.info(f"Enabled '{debugger}' debugger.")

        sys.stderr = stderr
