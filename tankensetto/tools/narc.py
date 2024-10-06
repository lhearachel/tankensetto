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

import abc
import pathlib

from tankensetto import tools


class NARC(abc.ABC):
    """
    Abstract contract for a tool which can pack and unpack Nitro Archive (NARC) files.
    """

    @abc.abstractmethod
    def unpack(self, path_to_narc: pathlib.Path, unpack_dir: pathlib.Path, force: bool) -> tools.Result:
        """
        Unpack a NARC's contents to the target directory.

        Arguments:
        path_to_narc -- path to the NARC file
        unpack_dir -- path to the inflation directory
        """
        pass


class Knarc(tools.Tool):
    """
    Implementation of NARC contract using lhearachel/knarc
    """

    def __init__(self) -> None:
        super().__init__(pathlib.Path("build/subprojects/knarc/knarc"), True)


    def unpack(self, narc: pathlib.Path, dir: pathlib.Path, force: bool=False) -> tools.Result:
        if dir.exists() and not force:
            return tools.Result.UNPACK_EXISTS

        dir.mkdir(parents=True, exist_ok=True)
        self.run([
            "-d", dir,
            "-u", narc,
        ])

        return tools.Result.SUCCESS


KNARC = Knarc()
