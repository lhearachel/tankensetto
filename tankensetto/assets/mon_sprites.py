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

import os
import pathlib
import shutil

import rich

from tankensetto import info
from tankensetto.constants import narc_path, pokemon
from tankensetto.tools import gfx, narc
from tankensetto.util import unpack_narcs


MON_DIRS = list(pokemon.Species)


def unpack_all(
    narc: narc.NARC,
    rom_filesys_root: pathlib.Path,
    force: bool,
) -> dict[narc_path.NARCPath, pathlib.Path]:
    all_narcs = [
        narc_path.NARCPath.pokegra,
    ]
    return unpack_narcs(narc, all_narcs, rom_filesys_root, force)


def convert_ncgr(gfx: gfx.GFX, ncgr: pathlib.Path, nclr: pathlib.Path, png: pathlib.Path):
    if os.stat(ncgr).st_size == 0:
        return

    gfx.ncgr_to_png(
        ncgr,
        png,
        nclr,
        extra_args=[
            "-scanfronttoback",
            "-handleempty",
        ],
    )


def convert_pokegra(
    contents: pathlib.Path,
    gfx: gfx.GFX,
    project_root: pathlib.Path,
):
    res_pokemon_root = project_root / "res" / "pokemon"
    rich.print("Converting sprites...")
    with info.PROGRESS_BAR as p:
        for i, species in p.track(enumerate(pokemon.Species), total=pokemon.MAX_SPECIES):
            j = i * 6
            mon_root = res_pokemon_root / species

            f_back = contents / f"{narc_path.NARCPath.pokegra.value.stem}_{j:08}.NCGR"
            m_back = contents / f"{narc_path.NARCPath.pokegra.value.stem}_{j+1:08}.NCGR"
            f_front = contents / f"{narc_path.NARCPath.pokegra.value.stem}_{j+2:08}.NCGR"
            m_front = contents / f"{narc_path.NARCPath.pokegra.value.stem}_{j+3:08}.NCGR"
            normal_pal = contents / f"{narc_path.NARCPath.pokegra.value.stem}_{j+4:08}.NCLR"
            shiny_pal = contents / f"{narc_path.NARCPath.pokegra.value.stem}_{j+5:08}.NCLR"

            shutil.copy(f_back.with_suffix(".bin"), f_back)
            shutil.copy(m_back.with_suffix(".bin"), m_back)
            shutil.copy(f_front.with_suffix(".bin"), f_front)
            shutil.copy(m_front.with_suffix(".bin"), m_front)
            shutil.copy(normal_pal.with_suffix(".bin"), normal_pal)
            shutil.copy(shiny_pal.with_suffix(".bin"), shiny_pal)

            convert_ncgr(gfx, f_back, normal_pal, mon_root / "female_back.png")
            convert_ncgr(gfx, m_back, normal_pal, mon_root / "male_back.png")
            convert_ncgr(gfx, f_front, normal_pal, mon_root / "female_front.png")
            convert_ncgr(gfx, m_front, normal_pal, mon_root / "male_front.png")

            if i == 0:
                shutil.copy(normal_pal, mon_root / "normal_pal.NCLR")
                shutil.copy(shiny_pal, mon_root / "shiny_pal.NCLR")
                continue

            gfx.nclr_to_pal(normal_pal, mon_root / "normal.pal", bitdepth=8)
            gfx.nclr_to_pal(shiny_pal, mon_root / "shiny.pal", bitdepth=8)


def extract(
    narc: narc.NARC,
    gfx: gfx.GFX,
    rom_filesys_root: pathlib.Path,
    project_root: pathlib.Path,
    force: bool,
):
    all_contents = unpack_all(narc, rom_filesys_root, force)

    convert_pokegra(all_contents[narc_path.NARCPath.pokegra], gfx, project_root)
