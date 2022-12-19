#!/usr/bin/python3

import argparse, datetime
import json
from pathlib import Path


class Format:
    END =       '\033[0m'
    BOLD =      '\033[1m'
    INVERT =    '\033[3m'
    UNDERLINE = '\033[4m'
    DARKCYAN =  '\033[36m'
    GRAY =      '\033[90m'
    RED =       '\033[91m'
    GREEN =     '\033[92m'
    YELLOW =    '\033[93m'
    BLUE =      '\033[94m'
    PURPLE =    '\033[95m'
    CYAN =      '\033[96m'


def info(msg, sep='\n'):
    print('{}-I-{} {}[ {} ]{} {}'.format(
        Format.GREEN, Format.END,
        Format.GRAY, Path(__file__).stem, Format.END,
        msg
    ), end=sep, flush=True)

def warning(msg):
    print('{}-W-{} {}[ {} ]{} {}'.format(
        Format.YELLOW, Format.END,
        Format.GRAY, Path(__file__).stem, Format.END,
        msg
    ))

def fatal(msg, err_code=1):
    print('{}-F-{} {}[ {} ]{} {}'.format(
        Format.RED, Format.END,
        Format.GRAY, Path(__file__).stem, Format.END,
        msg
    ))
    exit(err_code)

def wide_help_formatter(formatter, w=120, h=36):
    try:
        kwargs = {'width': w, 'max_help_position': h}
        formatter(None, **kwargs)
        return lambda prog: formatter(prog, **kwargs)
    except TypeError:
        return formatter

def getArgs():
    ap = argparse.ArgumentParser(
        add_help=False,
        formatter_class=wide_help_formatter(argparse.MetavarTypeHelpFormatter)
    )
    ap.description = f'Utility for setting up a new short story in LaTeX. Based on {Format.DARKCYAN}.defaults{Format.END} and {Format.DARKCYAN}template{Format.END}, a personalized LaTeX starting point is realized. If the provided title exists, then a new version is created.'

    arg = ap.add_argument_group('Arguments')
    xor = arg.add_mutually_exclusive_group(required=True)
    xor.add_argument('-t', '--title', type=str, help='Title of new project.', default=None)
    xor.add_argument('-k', '--ikey', type=str, help='JSON key (title) from story-ideas.json file.', default=None)
    arg.add_argument('-a', '--author', type=str, default=None, help='Author override. If not provided, one stored in .defaults used.')
    arg.add_argument('-s', '--synopsys', type=str, default='', help='Brief synopsys of story that will be commented out in TeX file. Only used in conjunction with title arg.')

    flg = ap.add_argument_group('Flags')
    flg.add_argument('-S', '--saveconfig', action='store_true', default=False, help='Save .defaults based on override values provided.')
    flg.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')

    return ap.parse_args()

def getFileContents(path):
    if path.exists():
        with open(str(path), 'r') as f:
            contents = f.read()
        return contents
    return None

def initConfig():
    kp = [
        ('author', 'Default author')
    ]

    config = {}
    for key, prompt in kp:
        config[key] = input(f'{prompt} '.ljust(49, '.') + ' ').title()

    return config

def main():
    args = getArgs()

    # load/set configs
    cpath = here / '.defaults'
    config = getFileContents(cpath)
    if config == None:
        args.saveconfig = True
        config = initConfig()
    else:
        config = json.loads(config)

    # override author
    if args.author != None:
        config['author'] = args.author.title()

    # load/set doc
    doc = {}
    ideas = getFileContents(here / 'story-ideas.json')
    ideas = json.loads(ideas)
    if args.title == None:
        args.ikey = args.ikey.lower()
        if args.ikey in ideas.keys():
            doc['title'] = args.ikey
            doc['synopsys'] = ideas[args.ikey]
        else:
            fatal(f'Provided ideas key [{Format.RED}{args.ikey}{Format.END}] not found.')
    else:
        doc['title'] = args.title
        doc['synopsys'] = args.synopsys

    # replace items in template
    kv = [
        ('##title##', doc['title'].title()),
        ('##author##', config['author']),
        ('##synopsys##', doc['synopsys'])
    ]
    newTeX = getFileContents(here / 'template')
    for key, val in kv:
        newTeX = newTeX.replace(key, val)

    # build directory structure
    name = doc['title'].replace(' ', '_').lower()
    name = ''.join(x for x in name if x.isalnum() or x == '_')
    spath = (here / name)
    n = 1
    if spath.exists():
        n = len(list(spath.iterdir())) + 1
    spath = spath / f'v{n}'
    spath.mkdir(parents=True)

    # write new TeX to file
    with open(str(spath / f'{name}_v{n}.tex'), 'w') as f:
        f.write(newTeX)

    # conditionally save config
    if args.saveconfig:
        with open(str(cpath), 'w') as f:
            f.write(json.dumps(config, indent=4))


if __name__ == '__main__':
    uniq = datetime.datetime.now().strftime('%m%d%y-%H%M%S')
    here = Path(__file__).resolve().parent
    main()
