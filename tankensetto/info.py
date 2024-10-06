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

import rich

from tankensetto import tools


def echo_result(result: tools.Result, src: str | pathlib.Path, dir: str | pathlib.Path) -> None:
    if result == tools.Result.UNPACK_EXISTS:
        rich.print(f"[bold cyan]🛈[/] [bold yellow]{dir}[/] exists; skipping unpack...")
    else:
        rich.print(f"[bold green]✓[/] Unpacked [bold yellow]{src}[/]")
