#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-09-08 23:08:04 krylon>
#
# /data/code/python/cleantags/scanner.py
# created on 08. 09. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of the PyKuang network scanner. It is distributed under the
# terms of the GNU General Public License 3. See the file LICENSE for details
# or find a copy online at https://www.gnu.org/licenses/gpl-3.0

"""
cleantags.scanner

(c) 2025 Benjamin Walkenhorst
"""

import logging
import os
import re
from dataclasses import dataclass
from queue import Queue
from typing import Final

from cleantags import common

audioPat: Final[re.Pattern] = re.compile("[.](?:mp3|ogg|opus|m4a|m4b)$", re.I)


@dataclass(slots=True, kw_only=True)
class Scanner:
    """Scanner looks for audio files whose metadata we might want to fix."""

    log: logging.Logger
    path: str
    fileQ: Queue[str]

    def __init__(self, path: str) -> None:
        self.path = path
        self.log = common.get_logger("scanner")
        self.fileQ = Queue()

    def visit_folder(self) -> None:
        """Visit the directory tree and scan for audio files."""
        for root, _folders, files in os.walk(self.path):
            for f in files:
                m = audioPat.search(f)
                if m is not None:
                    full_path = os.path.join(root, f)
                    self.fileQ.put(full_path)

# Local Variables: #
# python-indent: 4 #
# End: #
