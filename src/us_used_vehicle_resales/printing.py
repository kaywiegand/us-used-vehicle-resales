"""
Projekt-lokale Print-Helfer (schlichte ASCII-Trennlinien) für die Notebooks.

``EdaNotes``/``notes`` sind ins gemeinsame Toolkit gewandert
(``from wgnd import EdaNotes, notes``). Diese ``print_*``-Funktionen bleiben
lokal, weil ``process.py`` sie nutzt.
"""

LINE_LEN = 40
LINE_SY_IN = '-'
LINE_SY_OU = '~'


def print_header(headline='WGND'):
    print("\n\n")
    print(LINE_SY_OU*LINE_LEN)
    print(headline.upper())
    print(LINE_SY_OU*LINE_LEN)


def print_title(title):
    print(f"\n{title}")
    print(LINE_SY_IN*LINE_LEN)


def print_footer():
    print(LINE_SY_OU*LINE_LEN)
    print("\n")


def print_seperator():
    print(LINE_SY_IN*LINE_LEN)
    print("\n")
