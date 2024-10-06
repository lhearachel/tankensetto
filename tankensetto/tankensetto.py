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

import click

from tankensetto import extractors, info
from tankensetto.extractors import EXTRACTORS
from tankensetto.tools.gfx import NitroGFX
from tankensetto.tools.narc import Knarc
from tankensetto.tools.nds import NDSTOOL


@click.command()
@click.help_option("-h", "--help")
@click.option(
    "-s", "--source-rom",
    prompt="Path to source ROM",
    type=pathlib.Path,
    help="Source ROM to be asset-mined.",
)
@click.option(
    "-t", "--target-repo",
    prompt="Path to your project",
    type=pathlib.Path,
    help="Target decomp project for dumping.",
)
@click.option(
    "-f", "--force",
    is_flag=True,
    default=False,
    help="If specified, requested archives will be re-extracted."
)
@click.argument(
    "assets",
    nargs=-1,
    type=extractors.AssetExtractor,
)
def main(source_rom: pathlib.Path,
         target_repo: pathlib.Path,
         force: bool,
         assets: tuple[extractors.AssetExtractor]):
    """
    A collection of data-mining utilities for DS Pokémon games.

    This tool is aimed at prospective users of the pret decompilation projects
    who have an existing binary hacking project. It will guide such a user
    through extracting modified assets into the decomp project structure.

    If any ASSETS are specified, then only the requested ASSETS will be
    extracted.
    """
    rom_contents = pathlib.Path(source_rom.name + '_contents')
    extract_result = NDSTOOL.extract(source_rom, rom_contents, force)
    info.echo_result(extract_result, source_rom.name, rom_contents.name)

    knarc = Knarc(target_repo)
    gfx = NitroGFX(target_repo)

    to_extract = assets if assets else tuple(extractors.AssetExtractor)
    for asset in to_extract:
        EXTRACTORS[asset](knarc, gfx, rom_contents / 'filesys', target_repo, force)
