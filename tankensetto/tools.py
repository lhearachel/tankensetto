"""
    tankensetto - A collection of data-mining utilities for DS Pokemon games.
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
#!/usr/bin/env python

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


class Knarc(Tool):
    def __init__(self) -> None:
        super().__init__(pathlib.Path("build/subprojects/knarc/knarc"), True)


class NitroGfx(Tool):
    def __init__(self) -> None:
        super().__init__(pathlib.Path("build/subprojects/nitrogfx/nitrogfx"), True)


class NDSTool(Tool):
    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__(pathlib.Path("tools/ndstool/ndstool"), False)

    def extract(self, rom: pathlib.Path, dir: pathlib.Path) -> None:
        """
        Extract the contents of a ROM file to a directory.

        Arguments:
        rom -- ROM file to be extracted.
        dir -- Directory for extracted contents.
        """
        dir.mkdir(parents=True, exist_ok=True)
        self.run([
            "-x",  rom,
            "-9",  dir / "arm9.bin",
            "-7",  dir / "arm7.bin",
            "-y9", dir / "y9.bin",
            "-y7", dir / "y7.bin",
            "-d",  dir / "filesys",
            "-y",  dir / "overlay",
            "-t",  dir / "banner.bin",
            "-h",  dir / "header.bin",
        ])


NDSTOOL = NDSTool()
