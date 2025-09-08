#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-09-09 00:01:54 krylon>
#
# /data/code/python/cleantags/tag.py
# created on 08. 09. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of the PyKuang network scanner. It is distributed under the
# terms of the GNU General Public License 3. See the file LICENSE for details
# or find a copy online at https://www.gnu.org/licenses/gpl-3.0

"""
cleantags.tag

(c) 2025 Benjamin Walkenhorst
"""


import logging
import os
import re
from queue import Queue
from typing import Final

import mutagen

from cleantags import common

DiscNoPat: Final[re.Pattern] = re.compile("(\\d+)\\s*/\\s*(\\d+)")


class Tagger:
    """Tagger inspects and possibly fixes the metadata of audio files."""

    __slots__ = [
        "log",
        "queue",
    ]

    log: logging.Logger
    queue: Queue

    def __init__(self, q: Queue) -> None:
        self.log = common.get_logger("tag")
        self.queue = q

    def process_files(self) -> None:
        """Handle the files as they fall out of the Queue."""
        while not self.queue.is_shutdown:
            audiofile: str = self.queue.get()
            self.log.debug("Process %s", audiofile)


# pylint: disable-msg=R0912
def read_tags(path: str) -> dict[str, str]:  # noqa
    """Attempt to extract metadata from an audio file.

    path is expected to be the full, absolute path.
    """
    try:
        meta = mutagen.File(path)
    except mutagen.MutagenError:
        return {}

    tags: dict[str, str] = {
        "artist": "",
        "album": "",
        "title": "",
        "ord1": "0",
        "ord2": "0",
    }

    if "artist" in meta:
        tags["artist"] = meta["artist"][0]
    elif "TPE1" in meta:
        tags["artist"] = meta["TPE1"].text[0]

    if "album" in meta:
        tags["album"] = meta["album"][0]
    elif "TALB" in meta:
        tags["album"] = meta["TALB"].text[0]
    else:
        tags["album"] = os.path.basename(os.path.dirname(path))

    if "title" in meta:
        tags["title"] = meta["title"][0]
    elif "TIT2" in meta:
        tags["title"] = meta["TIT2"].text[0]

    if "tracknumber" in meta:
        tags["ord2"] = meta["tracknumber"][0]
    elif "TRCK" in meta:
        tags["ord2"] = meta["TRCK"].text[0]

    if "discnumber" in meta:
        tags["ord1"] = meta["discnumber"][0]
    elif "TPOS" in meta:
        tags["ord1"] = meta["TPOS"].text[0]

    m1 = DiscNoPat.search(tags["ord1"])
    if m1 is not None:
        tags["ord1"] = m1[1]

    m2 = DiscNoPat.search(tags["ord2"])
    if m2 is not None:
        tags["ord2"] = m2[1]

    return tags


# Local Variables: #
# python-indent: 4 #
# End: #
