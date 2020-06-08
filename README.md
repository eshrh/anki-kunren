# Anki Kunren (暗記 訓練)
Anki Kunren is a program to drill kanji stroke order and practice writing in sync with an Anki study session.
This is a work in progress

## Installation
I plan to publish this is a pypi module soon.

Currently, you can:
1. clone this repository: `git clone https://github.com/eshrh/anki-kunren`
2. install dependencies: `pip install pygame svg.path`
3. install [anki-connect](https://ankiweb.net/shared/info/2055492159) with code `2055492159`
5. run with kunren.py.

## Usage
usage: `kunren.py [-h] [-s S] [-d D] [--field FIELD]`

optional arguments:
+ `-h, --help` Show help message
+ `-s S` Start point size in px. default 5px
+ `-d D` Stroke forgiveness in average px from actual. default 25px
+ `--field FIELD` name of anki card field containing kanji. defaults to "Expression"

While running, you can use the following controls:
+ `h`: hint the current stroke
+ `n`: next kanji in the expression
+ `esc`: quit

## Other
This project uses KanjiVG stroke order data.
It is licensed by Ulrich Apel under the [Creative Commons Attribution Share-Alike 3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.

The KanjiVG reading code is taken from [Kanji Colorizer](https://github.com/cayennes/kanji-colorize) which is also the source of my initial inspiration
