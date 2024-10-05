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

```
make
```

Then, to access it:

```bash
source .venv/bin/activate
```
