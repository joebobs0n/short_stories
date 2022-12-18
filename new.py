#!/usr/bin/python3

import argparse, datetime
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
    ap.description = ''

    arg = ap.add_argument_group('Arguments')

    flg = ap.add_argument_group('Flags')
    flg.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                     help='Show this help message and exit.')

    return ap.parse_args()

def main():
    args = getArgs()

if __name__ == '__main__':
    uniq = datetime.datetime.now().strftime('%m%d%y-%H%M%S')
    main()
