#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-09-09 16:17:27 krylon>
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
import re
from queue import Queue
from typing import Final

import mutagen

from cleantags import common

DiscNoPat: Final[re.Pattern] = re.compile("(\\d+)\\s*/\\s*(\\d+)")
doublePat: Final[re.Pattern] = re.compile(r"^(.*?) / \1$")

tagNames: Final[tuple[str, ...]] = (
    "artist",
    "TPE1",
    "album",
    "TALB",
    "title",
    "TIT2",
)


class Tagger:
    """Tagger inspects and possibly fixes the metadata of audio files."""

    __slots__ = [
        "log",
        "queue",
        "dryRun",
    ]

    log: logging.Logger
    dryRun: bool
    queue: Queue

    def __init__(self, q: Queue, dryRun: bool = True) -> None:
        self.log = common.get_logger("tag")
        self.queue = q
        self.dryRun = dryRun

    def process_files(self) -> None:
        """Handle the files as they fall out of the Queue."""
        if self.dryRun:
            self.log.info("Dry run, won't modify any files.")

        while not self.queue.is_shutdown:
            audiofile: str = self.queue.get()
            self.log.debug("Process %s", audiofile)
            try:
                meta = mutagen.File(audiofile)
            except mutagen.MutagenError as err:
                self.log.error("Cannot read metadata from %s: %s",
                               audiofile,
                               err)

            fixCnt: int = 0
            for name in tagNames:
                if name in meta:
                    m = doublePat.match(meta.tags[name].text[0])
                    if m is not None:
                        fixed = m[1]
                        if not self.dryRun:
                            meta.tags[name].text[0] = fixed
                        fixCnt += 1

            if fixCnt > 0:
                try:
                    if not self.dryRun:
                        meta.save()
                except mutagen.MutagenError as err:
                    self.log.error("Failed to save metadata on %s: %s",
                                   audiofile,
                                   err)
                else:
                    self.log.info("Fixed %d metadata fields on %s",
                                  fixCnt,
                                  audiofile)


# # pylint: disable-msg=R0912
# def read_tags(path: str) -> dict[str, str]:  # noqa
#     """Attempt to extract metadata from an audio file.

#     path is expected to be the full, absolute path.
#     """
#     try:
#         meta = mutagen.File(path)
#     except mutagen.MutagenError:
#         return {}

#     tags: dict[str, str] = {}

#     if "artist" in meta:
#         tags["artist"] = meta["artist"][0]
#     if "TPE1" in meta:
#         tags["TPE1"] = meta["TPE1"].text[0]
#     if "album" in meta:
#         tags["album"] = meta["album"][0]
#     if "TALB" in meta:
#         tags["TALB"] = meta["TALB"].text[0]
#     if "title" in meta:
#         tags["title"] = meta["title"][0]
#     if "TIT2" in meta:
#         tags["TIT2"] = meta["TIT2"].text[0]

#     # if "tracknumber" in meta:
#     #     tags["ord2"] = meta["tracknumber"][0]
#     # elif "TRCK" in meta:
#     #     tags["ord2"] = meta["TRCK"].text[0]

#     # if "discnumber" in meta:
#     #     tags["ord1"] = meta["discnumber"][0]
#     # elif "TPOS" in meta:
#     #     tags["ord1"] = meta["TPOS"].text[0]

#     # m1 = DiscNoPat.search(tags["ord1"])
#     # if m1 is not None:
#     #     tags["ord1"] = m1[1]

#     # m2 = DiscNoPat.search(tags["ord2"])
#     # if m2 is not None:
#     #     tags["ord2"] = m2[1]

#     return tags


# Local Variables: #
# python-indent: 4 #
# End: #
