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


class NDS(abc.ABC):
    """
    Abstract contract for a tool which can pack and unpack Nitro Archive (NARC) files.
    """

    @abc.abstractmethod
    def extract(
        self, path_to_rom: pathlib.Path, unpack_dir: pathlib.Path, force: bool = False
    ) -> tools.Result:
        """
        Unpack a NARC's contents to the target directory.

        Arguments:
        path_to_rom -- path to the ROM file
        unpack_dir -- path to the inflation directory
        """
        pass


class NDSTool(NDS, tools.Tool):
    """
    Implementation of NDS contract using devkitpro/ndstool
    """

    def __init__(self) -> None:
        super().__init__(pathlib.Path("tools/ndstool/ndstool"))

    def extract(
        self, path_to_rom: pathlib.Path, unpack_dir: pathlib.Path, force: bool = False
    ) -> tools.Result:
        if unpack_dir.exists() and not force:
            return tools.Result.UNPACK_EXISTS

        unpack_dir.mkdir(parents=True, exist_ok=True)
        self.run(
            [
                "-x",
                path_to_rom,
                "-9",
                unpack_dir / "arm9.bin",
                "-7",
                unpack_dir / "arm7.bin",
                "-y9",
                unpack_dir / "y9.bin",
                "-y7",
                unpack_dir / "y7.bin",
                "-d",
                unpack_dir / "filesys",
                "-y",
                unpack_dir / "overlay",
                "-t",
                unpack_dir / "banner.bin",
                "-h",
                unpack_dir / "header.bin",
            ]
        )

        return tools.Result.SUCCESS


NDSTOOL = NDSTool()
