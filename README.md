# Anki Kunren (暗記 訓練)
Anki Kunren is a program to drill japanese kanji stroke order and practice writing in sync with an Anki study session.
This is a work in progress.

## Installation
1. install via pip: `pip install anki-kunren`
2. install [anki-connect](https://ankiweb.net/shared/info/2055492159) with code `2055492159`


## Usage
**Open Anki and begin a review. You can then use `kunren` as follows:**

usage: `kunren [-h] [-s S] [-d D] [--field FIELD]`

optional arguments:
+ `-h, --help` Show help message
+ `-s S` Start point size in px. defaults to 5px
+ `-d D` Stroke forgiveness in average px from actual. defaults to 25px
+ `--field FIELD` name of anki card field containing kanji. defaults to "Expression"
+ `--size SIZE` Length of a size of the square canvas in pixels. Defaults to 300.

While running, you can use the following controls:
+ `h`: hint the current stroke
+ `n`: next kanji in the expression
+ `esc`: quit

## Other
This project uses KanjiVG stroke order data.
It is licensed by Ulrich Apel under the [Creative Commons Attribution Share-Alike 3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.

The KanjiVG ascii filename code is taken from [Kanji Colorizer](https://github.com/cayennes/kanji-colorize) which was also the source of my initial inspiration.

## TODO
+ catch all indexoutofbounds
+ smoother kanji lines
+ different coloring for different parts of stroke based on how wrong it is.
