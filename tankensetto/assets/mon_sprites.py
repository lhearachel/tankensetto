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

import dataclasses
import os
import pathlib
import shutil

import rich

from tankensetto import info
from tankensetto.constants import narc_path, pokemon
from tankensetto.tools import gfx, narc
from tankensetto.util import unpack_narcs


@dataclasses.dataclass
class AltFormSpriteSet:
    normal_pal: int
    shiny_pal: int
    back: int
    front: int


MON_DIRS = list(pokemon.Species)

OTHERPOKE_FILES: dict[pokemon.Species, dict[str, AltFormSpriteSet]] = {
    pokemon.Species.deoxys: {
        "base": AltFormSpriteSet(154, 155, 0, 1),
        "attack": AltFormSpriteSet(154, 155, 2, 3),
        "defense": AltFormSpriteSet(154, 155, 4, 5),
        "speed": AltFormSpriteSet(154, 155, 6, 7),
    },
    pokemon.Species.unown: {
        "base": AltFormSpriteSet(156, 157, 8, 9),
        "b": AltFormSpriteSet(156, 157, 10, 11),
        "c": AltFormSpriteSet(156, 157, 12, 13),
        "d": AltFormSpriteSet(156, 157, 14, 15),
        "e": AltFormSpriteSet(156, 157, 16, 17),
        "f": AltFormSpriteSet(156, 157, 18, 19),
        "g": AltFormSpriteSet(156, 157, 20, 21),
        "h": AltFormSpriteSet(156, 157, 22, 23),
        "i": AltFormSpriteSet(156, 157, 24, 25),
        "j": AltFormSpriteSet(156, 157, 26, 27),
        "k": AltFormSpriteSet(156, 157, 28, 29),
        "l": AltFormSpriteSet(156, 157, 30, 31),
        "m": AltFormSpriteSet(156, 157, 32, 33),
        "n": AltFormSpriteSet(156, 157, 34, 35),
        "o": AltFormSpriteSet(156, 157, 36, 37),
        "p": AltFormSpriteSet(156, 157, 38, 39),
        "q": AltFormSpriteSet(156, 157, 40, 41),
        "r": AltFormSpriteSet(156, 157, 42, 43),
        "s": AltFormSpriteSet(156, 157, 44, 45),
        "t": AltFormSpriteSet(156, 157, 46, 47),
        "u": AltFormSpriteSet(156, 157, 48, 49),
        "v": AltFormSpriteSet(156, 157, 50, 51),
        "w": AltFormSpriteSet(156, 157, 52, 53),
        "x": AltFormSpriteSet(156, 157, 54, 55),
        "y": AltFormSpriteSet(156, 157, 56, 57),
        "z": AltFormSpriteSet(156, 157, 58, 59),
        "exc": AltFormSpriteSet(156, 157, 60, 61),
        "que": AltFormSpriteSet(156, 157, 62, 63),
    },
    pokemon.Species.castform: {
        "base": AltFormSpriteSet(158, 162, 64, 68),
        "sunny": AltFormSpriteSet(159, 163, 65, 69),
        "rainy": AltFormSpriteSet(160, 164, 66, 70),
        "snowy": AltFormSpriteSet(161, 165, 67, 71),
    },
    pokemon.Species.burmy: {
        "base": AltFormSpriteSet(166, 167, 72, 73),
        "sandy": AltFormSpriteSet(168, 169, 74, 75),
        "trash": AltFormSpriteSet(170, 171, 76, 77),
    },
    pokemon.Species.wormadam: {
        "base": AltFormSpriteSet(172, 173, 78, 79),
        "sandy": AltFormSpriteSet(174, 175, 80, 81),
        "trash": AltFormSpriteSet(176, 177, 82, 83),
    },
    pokemon.Species.shellos: {
        "base": AltFormSpriteSet(178, 179, 84, 86),
        "east_sea": AltFormSpriteSet(180, 181, 85, 87),
    },
    pokemon.Species.gastrodon: {
        "base": AltFormSpriteSet(182, 183, 88, 90),
        "east_sea": AltFormSpriteSet(184, 185, 89, 91),
    },
    pokemon.Species.cherrim: {
        "base": AltFormSpriteSet(186, 188, 92, 94),
        "sunny": AltFormSpriteSet(187, 189, 93, 95),
    },
    pokemon.Species.arceus: {
        "base": AltFormSpriteSet(190, 191, 96, 97),
        "fighting": AltFormSpriteSet(192, 193, 98, 99),
        "flying": AltFormSpriteSet(194, 195, 100, 101),
        "poison": AltFormSpriteSet(196, 197, 102, 103),
        "ground": AltFormSpriteSet(198, 199, 104, 105),
        "rock": AltFormSpriteSet(200, 201, 106, 107),
        "bug": AltFormSpriteSet(202, 203, 108, 109),
        "ghost": AltFormSpriteSet(204, 205, 110, 111),
        "steel": AltFormSpriteSet(206, 207, 112, 113),
        "mystery": AltFormSpriteSet(208, 209, 114, 115),
        "fire": AltFormSpriteSet(210, 211, 116, 117),
        "water": AltFormSpriteSet(212, 213, 118, 119),
        "grass": AltFormSpriteSet(214, 215, 120, 121),
        "electric": AltFormSpriteSet(216, 217, 122, 123),
        "psychic": AltFormSpriteSet(218, 219, 124, 125),
        "ice": AltFormSpriteSet(220, 221, 126, 127),
        "dragon": AltFormSpriteSet(222, 223, 128, 129),
        "dark": AltFormSpriteSet(224, 225, 130, 131),
    },
    # pokemon.Species.egg: {}, -- special handling
    pokemon.Species.shaymin: {
        "base": AltFormSpriteSet(228, 229, 134, 135),
        "sky": AltFormSpriteSet(230, 231, 136, 137),
    },
    pokemon.Species.rotom: {
        "base": AltFormSpriteSet(232, 233, 138, 139),
        "heat": AltFormSpriteSet(234, 235, 140, 141),
        "wash": AltFormSpriteSet(236, 237, 142, 143),
        "frost": AltFormSpriteSet(238, 239, 144, 145),
        "fan": AltFormSpriteSet(240, 241, 146, 147),
        "mow": AltFormSpriteSet(242, 243, 148, 149),
    },
    pokemon.Species.giratina: {
        "base": AltFormSpriteSet(244, 245, 150, 151),
        "origin": AltFormSpriteSet(246, 247, 152, 153),
    },
}


def unpack_all(
    narc: narc.NARC,
    rom_filesys_root: pathlib.Path,
    force: bool,
) -> dict[narc_path.NARCPath, pathlib.Path]:
    all_narcs = [
        narc_path.NARCPath.pokegra,
        narc_path.NARCPath.otherpoke,
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
    rich.print("Converting base form sprites...")
    with info.progress() as p:
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


def convert_otherpoke(
    contents: pathlib.Path,
    gfx: gfx.GFX,
    project_root: pathlib.Path,
):
    res_pokemon_root = project_root / "res" / "pokemon"
    egg_root = res_pokemon_root / "egg"
    shared_root = res_pokemon_root / ".shared"

    rich.print("Converting alt form sprites...")

    egg_base = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_00000132.NCGR"
    egg_manaphy = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_00000133.NCGR"
    egg_base_pal = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_00000226.NCLR"
    egg_manaphy_pal = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_00000227.NCLR"
    [shutil.copy(f.with_suffix(".bin"), f) for f in [egg_base, egg_manaphy, egg_base_pal, egg_manaphy_pal]]

    convert_ncgr(gfx, egg_base, egg_base_pal, egg_root / "front.png")
    convert_ncgr(gfx, egg_manaphy, egg_manaphy_pal, egg_root / "forms" / "manaphy" / "front.png")
    gfx.nclr_to_pal(egg_base_pal, egg_root / "normal.pal", bitdepth=8)
    gfx.nclr_to_pal(egg_manaphy_pal, egg_root / "forms" / "manaphy" / "normal.pal", bitdepth=8)

    sub_back = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_00000248.NCGR"
    sub_front = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_00000249.NCGR"
    sub_pal = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_00000250.NCLR"
    [shutil.copy(f.with_suffix(".bin"), f) for f in [sub_back, sub_front, sub_pal]]

    convert_ncgr(gfx, sub_back, sub_pal, shared_root / "substitute_back.png")
    convert_ncgr(gfx, sub_front, sub_pal, shared_root / "substitute_front.png")
    gfx.nclr_to_pal(sub_pal, shared_root / "substitute.pal", bitdepth=8)

    shadows_img = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_00000251.NCGR"
    shadows_pal = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_00000252.NCLR"
    [shutil.copy(f.with_suffix(".bin"), f) for f in [shadows_img, shadows_pal]]
    convert_ncgr(gfx, shadows_img, shadows_pal, shared_root / "shadows.png")
    gfx.nclr_to_pal(shadows_pal, shared_root / "shadows.pal", bitdepth=8)

    with info.progress() as p:
        for species, forms in p.track(OTHERPOKE_FILES.items()):
            mon_root = res_pokemon_root / species / 'forms'
            mon_shared_pal = None

            for form, sprites in forms.items():
                form_dir = mon_root / form

                back = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_{sprites.back:08}.NCGR"
                front = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_{sprites.front:08}.NCGR"
                normal = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_{sprites.normal_pal:08}.NCLR"
                shiny = contents / f"{narc_path.NARCPath.otherpoke.value.stem}_{sprites.shiny_pal:08}.NCLR"

                [shutil.copy(f.with_suffix(".bin"), f) for f in [back, front, normal, shiny]]

                convert_ncgr(gfx, back, normal, form_dir / "back.png")
                convert_ncgr(gfx, front, normal, form_dir / "front.png")

                if not mon_shared_pal:
                    mon_shared_pal = normal
                elif mon_shared_pal != normal:
                    gfx.nclr_to_pal(normal, form_dir / "normal.pal", bitdepth=8)
                    gfx.nclr_to_pal(shiny, form_dir / "shiny.pal", bitdepth=8)


def convert_poke_data(
    contents: pathlib.Path,
    project_root: pathlib.Path
):
    pass


def convert_height(
    contents: pathlib.Path,
    project_root: pathlib.Path
):
    pass


def convert_poke_icon(
    contents: pathlib.Path,
    gfx: gfx.GFX,
    project_root: pathlib.Path
):
    pass


def extract(
    narc: narc.NARC,
    gfx: gfx.GFX,
    rom_filesys_root: pathlib.Path,
    project_root: pathlib.Path,
    force: bool,
):
    all_contents = unpack_all(narc, rom_filesys_root, force)

    convert_pokegra(all_contents[narc_path.NARCPath.pokegra], gfx, project_root)
    convert_otherpoke(all_contents[narc_path.NARCPath.otherpoke], gfx, project_root)
    convert_poke_data(all_contents[narc_path.NARCPath.poke_data], project_root)
    convert_height(all_contents[narc_path.NARCPath.height], project_root)
    convert_poke_icon(all_contents[narc_path.NARCPath.poke_icon], gfx, project_root)
