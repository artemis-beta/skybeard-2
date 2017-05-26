#!/usr/bin/env python

import argparse
from pathlib import Path
from shutil import copytree

from utils import make_init_text


def make_readme(dir_, name):
    readme_text = """A beard named {} for skybeard-2.""".format(name)
    with (dir_ / Path("README.txt")).open("w") as f:
        f.write(readme_text)


def make_init(dir_, name):
    python_path = dir_ / Path("python/{}".format(name))
    python_path.mkdir(parents=True)

    init_text = make_init_text(name)

    with (python_path / Path("__init__.py")).open("w") as f:
        f.write(init_text)


def make_setup_beard(dir_, name):
    setup_beard_text = '''
from skybeard.utils import setup_beard

setup_beard(
    "{}",
)

    '''.format(name).strip()

    with (dir_ / Path("setup_beard.py")).open("w") as f:
        f.write(setup_beard_text)


def copy_existing_old_style_beard(dir_, directory):
    pythonpath = str(dir_ / "python/")
    copytree(directory, pythonpath)


def make_requirements(dir_, requirements):
    requirements_text = "\n".join(requirements)

    with (dir_ / Path("requirements.txt")).open("w") as f:
        f.write(requirements_text)


def main():
    parser = argparse.ArgumentParser(
        description='Create new beard in given folder.')
    parser.add_argument('name', help="Name of beard.")
    parser.add_argument(
        '-d', '--dir', type=Path, default=None,
        help="Directory to put beard in (defaults to beard name).")
    parser.add_argument(
        '-r', '--requirements', default=None,
        help="Create requirements file with optional requirements.", nargs="*")
    parser.add_argument('-u', '--upgrade',
                        help="Upgrades an existing beard to a new style beard.",
                        type=str,
                        default=None)

    parsed = parser.parse_args()

    if parsed.dir is None:
        parsed.dir = Path(parsed.name)

    try:
        parsed.dir.mkdir(parents=True)
    except FileExistsError:
        pass

    make_readme(parsed.dir, parsed.name)
    if parsed.upgrade is None:
        make_init(parsed.dir, parsed.name)
    else:
        copy_existing_old_style_beard(parsed.dir, parsed.upgrade)
    make_setup_beard(parsed.dir, parsed.name)
    if parsed.requirements is not None:
        make_requirements(parsed.dir, parsed.requirements, parsed.upgrade)


if __name__ == '__main__':
    main()
