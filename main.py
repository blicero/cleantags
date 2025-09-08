#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-09-08 23:07:54 krylon>
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
from queue import Queue
from threading import Thread

from cleantags.scanner import Scanner


def main() -> None:
    """Run our humble application."""
    argp: argparse.ArgumentParser = argparse.ArgumentParser()
    argp.add_argument("-p", "--path", help="The path to scan for audio files")

    args = argp.parse_args()

    sc: Scanner = Scanner(args.path)
    worker = Thread(target=handle_files, args=(sc.fileQ, ), daemon=True)
    worker.start()
    sc.visit_folder()


def handle_files(q: Queue) -> None:
    """Process the files discovered by the Scanner."""
    while True:
        f: str = q.get()
        print(f)

# Local Variables: #
# python-indent: 4 #
# End: #
