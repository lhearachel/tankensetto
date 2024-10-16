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

import pathlib
from typing import Literal

from tankensetto import info
from tankensetto.constants import narc_path
from tankensetto.tools import narc


def full_stem(path: pathlib.Path) -> pathlib.Path:
    """
    Returns the parent of the given path + its stem.

    e.g., full_stem("this/is/a/file.txt") -> "this/is/a/file"
    """
    return path.parent / path.stem


def unpack_narc(
    narc: narc.NARC,
    path: narc_path.NARCPath,
    rom_filesys_root: pathlib.Path,
    force: bool = True,
    echo: bool = True,
) -> pathlib.Path:
    """
    Unpacks a NARC to a contents directory and optionally echoes the result.

    Returns the path to the unpacked contents directory.
    """
    contents = rom_filesys_root / f"{full_stem(path.value)}_contents"
    unpack_result = narc.unpack(rom_filesys_root / path.value, contents, force)

    if echo:
        info.echo_result(unpack_result, path.name, contents.name)

    return contents


def unpack_narcs(
    narc: narc.NARC,
    paths: list[narc_path.NARCPath],
    rom_filesys_root: pathlib.Path,
    force: bool = True,
    echo: bool = True,
) -> dict[narc_path.NARCPath, pathlib.Path]:
    """
    Unpack a list of NARCs to contents directories, optionally echoing each result.

    Returns a mapping of input NARCs to their unpacked contents directories.
    """
    return {np: unpack_narc(narc, np, rom_filesys_root, force, echo) for np in paths}


def le_int(b: bytes) -> int:
    """
    Short stub func to convert bytes to an int from little Endian.
    """
    return int.from_bytes(b, byteorder="little")


def sint8(b: int | bytes):
    i = int(b)
    return i - 256 if i >= 128 else i
