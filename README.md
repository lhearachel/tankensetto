# `tankensetto`

`tankensetto` is a managed collection of utilities for extracting assets from
Generation 4 Pokémon games into more common formats used by the `pret`
decompilation projects.

Currently, only [`pret/pokeplatinum`](https://github.com/pret/pokeplatinum) is
supported.

## Setup

This tool assumes that you have installed all the dependencies required to
build a `pret` decompilation project and that you have already compiled a
matching ROM to verify your project setup.

`tankensetto` requires a minimum of Python version 3.10.

To create an executable, simply run the following command:

```bash
make
```

Then, to access it:

```bash
source .venv/bin/activate
```

## Usage

After activating the environment, you can verify that you are able to use the
tool like so:

```console
$ tankensetto --help
Usage: tankensetto [OPTIONS] [ASSETS]...

  A collection of data-mining utilities for DS Pokémon games.

  This tool is aimed at prospective users of the pret decompilation projects
  who have an existing binary hacking project. It will guide such a user
  through extracting modified assets into the decomp project structure.

  If any ASSETS are specified, then only the requested ASSETS will be
  extracted.

Options:
  -h, --help              Show this message and exit.
  -s, --source-rom PATH   Source ROM to be asset-mined.
  -t, --target-repo PATH  Target decomp project for dumping.
  -f, --force             If specified, requested archives will be re-
                          extracted.

  Possible values for ASSETS: ['mon_sprites']
```

For a first-time use, you should not need to specify any values for `ASSETS`;
to run through all data-mining procedures:

```bash
tankensetto -s <path/to/your/source/rom.nds> -t <path/to/your/decomp/project>
```
