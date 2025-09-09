#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-09-09 16:21:10 krylon>
#
# /data/code/python/cleantags/main.py
# created on 08. 09. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of the PyKuang network scanner. It is distributed under the
# terms of the GNU General Public License 3. See the file LICENSE for details
# or find a copy online at https://www.gnu.org/licenses/gpl-3.0

"""
cleantags.main

(c) 2025 Benjamin Walkenhorst
"""


import argparse
import logging
from queue import Queue
from threading import Thread

from cleantags import common
from cleantags.scanner import Scanner
from cleantags.tag import Tagger


def main() -> None:
    """Run our humble application."""
    argp: argparse.ArgumentParser = argparse.ArgumentParser()
    argp.add_argument("-p", "--path", help="The path to scan for audio files")
    argp.add_argument("-n", "--dry-run",
                      action="store_true",
                      default=True,
                      help="Dry run, do not modify any files")

    args = argp.parse_args()

    sc: Scanner = Scanner(args.path)
    t: Tagger = Tagger(sc.fileQ, args.dry_run)
    worker = Thread(target=t.process_files, daemon=True)
    worker.start()
    sc.visit_folder()


def handle_files(q: Queue) -> None:
    """Process the files discovered by the Scanner."""
    try:
        log: logging.Logger = common.get_logger("main")
        while not q.is_shutdown:
            f: str = q.get()
            log.debug("Found file %s", f)
    finally:
        log.debug("File handler is done. Toodles!")


if __name__ == '__main__':
    main()

# Local Variables: #
# python-indent: 4 #
# End: #
