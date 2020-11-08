#!/usr/bin/env python3
import sys

if sys.version_info.major != 3:
    print('please run with python 3')
    sys.exit(1)

from pathlib import Path
import os
import logging
import getopt

logging.basicConfig(format='%(levelname)s %(message)s', level=logging.INFO)

SOURCE_DIR = str(Path().absolute())
TARGET_DIR = str(os.environ['HOME'])
IGNORE_SET = {os.path.basename(__file__)}
REPLACE = False
SOFTLINKS = False
QUIET = False


# https://www.python.org/dev/peps/pep-0616/#specification
def removeprefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix):]
    else:
        return text[:]


# https://www.python.org/dev/peps/pep-0616/#specification
def removesuffix(text: str, suffix: str) -> str:
    if text and text.endswith(suffix):
        return text[:-len(suffix)]
    else:
        return text[:]


def process_args(args):
    help_message = """reclink - link files recursively
-r, --replace               replace existing targets
-l, --links                 link to softlinks
-q, --quiet                 skip user confirmation
-s, --source {{PATH}}       path to source directory
-t, --target {{PATH}}       path to target directory
-i, --ignore {{PATH,PATH}}  relative paths to be ignored
-h, --help                  display this help message and exit
-v, --version               display version message and exit"""
    try:
        opts, _ = getopt.getopt(args,
                                "rlqs:t:i:hv",
                                ["replace",
                                 "links",
                                 "quiet",
                                 "source=",
                                 "target=",
                                 "ignore=",
                                 "help",
                                 "version"])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-r", "--replace"):
            global REPLACE
            REPLACE = True
        elif opt in ("-l", "--links"):
            global SOFTLINKS
            SOFTLINKS = True
        elif opt in ("-q", "--quiet"):
            global QUIET
            QUIET = True
        elif opt in ("-s", "--source"):
            global SOURCE_DIR
            SOURCE_DIR = os.path.abspath(arg)
        elif opt in ("-t", "--target"):
            global TARGET_DIR
            TARGET_DIR = os.path.abspath(arg)
        elif opt in ("-i", "--ignore"):
            global IGNORE_SET
            for i in str(arg).split(','):
                IGNORE_SET.add(i.lstrip())
        elif opt in ("-h", "--help"):
            print(help_message)
            sys.exit(0)
        elif opt in ("-v", "--version"):
            print("reclink 1.1")
            sys.exit(0)


def link_file(source: str):
    # check source
    if not SOFTLINKS and os.path.islink(source):
        logging.warning('skipping link, source is a link: ' + source)
        return
    # absolute path
    target = os.path.abspath(TARGET_DIR + os.sep + removeprefix(text=source, prefix=SOURCE_DIR))
    # check target
    if os.path.exists(target):
        if not REPLACE:
            logging.info('skipping link, target already exists: ' + target)
            return
        if os.path.isdir(target):
            logging.warning('skipping link, target is a directory: ' + target)
            return
        elif os.path.isfile(target) or os.path.islink(target):
            os.remove(target)
    else:
        if not os.path.isdir(os.path.abspath(target + os.sep + '..')):
            logging.info('creating directories for file: ' + target)
            try:
                os.makedirs(removesuffix(target, os.path.basename(os.sep + target)), mode=0o755, exist_ok=True)
            except FileExistsError:
                logging.warning('unable to create directory at: ' + os.path.abspath(target + os.sep + '..'))
                return
    logging.info('linking file: ' + source + ' to ' + target)
    # create softlink
    os.symlink(source, target)


def is_ignored(abs_path: str):
    rel_path = removeprefix(text=abs_path, prefix=SOURCE_DIR + os.sep)
    for i in IGNORE_SET:
        if rel_path == i or rel_path.startswith(i + os.sep):
            return True
    return False


if __name__ == '__main__':

    process_args(sys.argv[1:])

    if not QUIET:
        print('source: ' + str(SOURCE_DIR))
        print('target: ' + str(TARGET_DIR))
        print('ignore: ' + str(sorted(IGNORE_SET)))
        input('press enter to confirm')

    if not os.path.isdir(SOURCE_DIR):
        logging.error('source is not a directory: ' + SOURCE_DIR)
        sys.exit(2)

    if not os.path.isdir(TARGET_DIR):
        logging.error('target is not a directory: ' + TARGET_DIR)
        sys.exit(2)

    if SOURCE_DIR == TARGET_DIR:
        logging.error('source and target directory can not be the same')
        sys.exit(2)

    for root, _, files in os.walk(SOURCE_DIR):
        if is_ignored(root):
            logging.info('ignoring folder: ' + str(root))
            continue
        for f in files:
            path = os.path.abspath(root + os.sep + f)
            if is_ignored(path):
                logging.info('ignoring file: ' + str(path))
                continue
            link_file(path)
