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


class GFX(abc.ABC):
    """
    Abstract contract for a tool which can convert Nitro graphics files to common media formats.
    """

    @abc.abstractmethod
    def ncgr_to_png(
        self,
        path_to_ncgr: pathlib.Path,
        path_to_png: pathlib.Path,
        path_to_nclr: pathlib.Path,
        pal_idx: int = 0,
        extra_args: list = [],
    ) -> tools.Result:
        """
        Convert an NCGR to a PNG, using the given NCLR as its palette.

        Arguments:
        path_to_ncgr -- path to the NCGR file
        path_to_png -- path to the output PNG file
        path_to_nclr -- path to NCLR palette to apply to the output PNG
        pal_idx -- index in the palette file to be used
        extra_args -- list of additional args
        """
        pass

    @abc.abstractmethod
    def nclr_to_pal(
        self,
        path_to_nclr: pathlib.Path,
        path_to_pal: pathlib.Path,
        bitdepth: int = 0,
        extra_args: list = [],
    ) -> tools.Result:
        """
        Convert an NCLR to a JASC PAL.

        Arguments:
        path_to_nclr -- path to the NCLR file
        path_to_pal -- path to the output PAL file
        bitdepth -- bitdepth for the palette
        extra_args -- list of additional args
        """

    @abc.abstractmethod
    def ncer_to_json(
        self,
        path_to_ncer: pathlib.Path,
        path_to_json: pathlib.Path,
    ) -> tools.Result:
        """
        Convert an NCER to JSON.
        """

    @abc.abstractmethod
    def nanr_to_json(
        self,
        path_to_nanr: pathlib.Path,
        path_to_json: pathlib.Path,
    ) -> tools.Result:
        """
        Convert an NANR to JSON.
        """


class NitroGFX(GFX, tools.Tool):
    """
    Implementation of GFX contract using red031000/nitrogfx
    """

    def __init__(self, parent: pathlib.Path) -> None:
        super().__init__(pathlib.Path("build/subprojects/nitrogfx/nitrogfx"), parent)

    def ncgr_to_png(
        self,
        path_to_ncgr: pathlib.Path,
        path_to_png: pathlib.Path,
        path_to_nclr: pathlib.Path,
        pal_idx: int = 0,
        extra_args: list = [],
    ) -> tools.Result:
        args = [
            path_to_ncgr,
            path_to_png,
            "-palette",
            path_to_nclr,
        ]

        if pal_idx != 0:
            args.extend(["-palindex", str(pal_idx)])

        args.extend(extra_args)

        self.run(args)
        return tools.Result.SUCCESS

    def nclr_to_pal(
        self,
        path_to_nclr: pathlib.Path,
        path_to_pal: pathlib.Path,
        bitdepth: int = 0,
        extra_args: list = [],
    ) -> tools.Result:
        args: list[str | pathlib.Path] = [
            path_to_nclr,
            path_to_pal,
        ]

        if bitdepth != 0:
            args.extend(["-bitdepth", str(bitdepth)])

        args.extend(extra_args)

        self.run(args)
        return tools.Result.SUCCESS

    def ncer_to_json(
        self,
        path_to_ncer: pathlib.Path,
        path_to_json: pathlib.Path,
    ) -> tools.Result:
        self.run([path_to_ncer, path_to_json])
        return tools.Result.SUCCESS

    def nanr_to_json(
        self,
        path_to_nanr: pathlib.Path,
        path_to_json: pathlib.Path,
    ) -> tools.Result:
        self.run([path_to_nanr, path_to_json])
        return tools.Result.SUCCESS
