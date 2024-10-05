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
#!/usr/bin/env python

import pathlib

import click

from tankensetto.tools import NDSTOOL


@click.command()
@click.help_option("-h", "--help")
@click.option(
    "-s", "--source-rom",
    prompt="Path to source ROM",
    type=pathlib.Path,
    help="Source ROM to be asset-mined."
)
@click.option(
    "-t", "--target-repo",
    prompt="Path to your project",
    type=pathlib.Path,
    help="Target decomp project for dumping."
)
def main(source_rom: pathlib.Path, target_repo: pathlib.Path):
    """
    A collection of data-mining utilities for DS Pokémon games.

    This tool is aimed at prospective users of the pret decompilation projects
    who have an existing binary hacking project. It will guide such a user
    through extracting modified assets into the decomp project structure.
    """
    rom_contents = pathlib.Path(source_rom.name + '_contents')
    NDSTOOL.extract(source_rom, rom_contents)

