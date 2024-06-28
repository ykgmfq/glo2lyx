# glo2lyx
Replace glossary keywords in LyX text with nomenclature commands.
## Installation
```
pip install https://github.com/ykgmfq/glo2lyx/archive/refs/tags/v1.zip
```

## Usage
An example glossary looks like this:
```tex
\usepackage[automake]{glossaries-extra}
\renewcommand{\nomenclature}[2]{\gls{#1}}
\makeglossaries
\newabbreviation{api}{API}{Application Programming Interface}
```
Include this file in your LyX document preamble.
Then you can use your abbreviation in the LyX editor with plain text:
```
We use an api for this task.
#api development is tedious.
```
Surround your abbreviation with spaces or lead with `#`.
After running `glo2lyx` the abbreviation will be properly added to your document!

## Why do I need this?
See
https://tex.stackexchange.com/questions/12346
