#!/usr/bin/env python
"""
    tankensetto - A collection of data-mining utilities for DS Pokémon games.
    Copyright (C) 2024  lhearachel@proton.me

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import enum
import pathlib
import subprocess


class Tool:
    """
    Abstraction of an external executable tool for the data-mining process.
    """

    def __init__(self, exe: pathlib.Path, in_proj: bool) -> None:
        """
        Constructor.

        Arguments:
        exe -- path component to the executable
        in_proj -- if True, then the given path is relative to the target project
        """
        self.exe = exe
        self.in_proj = in_proj

    def run(self, args: list[str | pathlib.Path]) -> None:
        """
        Thin wrapper around Popen against the executable.

        Arguments:
        args -- additional args to the process
        """
        with subprocess.Popen([self.exe, *args]) as proc:
            proc.wait()
            assert proc.returncode == 0


class Result(enum.IntEnum):
    SUCCESS = enum.auto()
    UNPACK_EXISTS = enum.auto()
