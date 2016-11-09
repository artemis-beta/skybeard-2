#!/usr/bin/env python
import os
import sys
import logging
import importlib
import argparse


import config

from skybeard.beards import Beard
import autoloaders
from help import create_help

logger = logging.getLogger(__name__)

def is_module(filename):
    fname, ext = os.path.splitext(filename)
    if ext == ".py":
        return True
    elif os.path.exists(os.path.join(filename, "__init__.py")):
        return True
    else:
        return False

def all_possible_beards(paths):
    for path in paths:
        for f in os.listdir(path):
            if is_module(os.path.join(path, f)):
                yield os.path.basename(f)

def get_literal_beard_paths(beard_paths):
    for beard_path in beard_paths:
        if issubclass(type(beard_path), autoloaders.AutoLoader):
            literal_beard_paths.insert(0, beard_path.path)
        else:
            literal_beard_paths.insert(0, beard_path)

    return literal_beard_paths


def main(config):
    literal_beard_paths = get_literal_beard_paths(config.beard_paths)

    for beard_path in literal_beard_paths:
        sys.path.insert(0, beard_path)

    logger.info("Loaded the following plugins:\n {}".format(
        ', '.join(list(all_possible_beards(literal_beard_paths)))))
    logger.info("config.beards: {}".format(config.beards))

    if config.beards == "all":
        for beard_name in all_possible_beards(config.beard_paths):
            importlib.import_module(beard_name)
    else:
        for beard_name in config.beards:
            importlib.import_module(beard_name)

    for beard_path in literal_beard_paths:
        sys.path.pop(0)

    updater = Beard.updater
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Skybeard hails you!')

    parser.add_argument('-k', '--key', default=os.environ.get('TG_BOT_TOKEN'))
    parser.add_argument('--no-help', action='store_true')
    parser.add_argument('-d', '--debug', action='store_const', dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    parsed = parser.parse_args()

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=parsed.loglevel)


    # Set up the master beard
    Beard.setup_beard(parsed.key)

    # If the user does not specially request --no-help, set up help command.
    if not parsed.no_help:
        create_help(config)

    logger.debug("Config found to be: {}".format(dir(config)))


    # TODO make an argparse here to override the config file (and also specify
    # the config file)
    main(config)
