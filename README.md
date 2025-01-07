# regenx

_regenx_ is yet another regex based text generation library


[![PyPI - Version](https://img.shields.io/pypi/v/regenx.svg)](https://pypi.org/project/regenx)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/regenx.svg)](https://pypi.org/project/regenx)

-----

## Table of Contents

- [regenx](#regenx)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Features](#features)
    - [Supported syntax](#supported-syntax)
  - [Limitations](#limitations)
  - [See also](#see-also)
  - [License](#license)

## Installation

```console
pip install regenx
```

## Features

This library currently supports generating all the possible strings that would match the given regex.

### Supported syntax

`.` character (it will include all ascii printable characters)
`\` escape sequences
all the special ones are ascii only
the negative (uppercase) special escapes will include all ascii printable characters minus the specified ones

- `\d` digits, same as `[0-9]`
- `\D` non digits, same as `[^0-9]`
- `\s` whitespace, same as `[ \t\n\r\f\v]`
- `\S` non whitespace, same as `[^ \t\n\r\f\v]`
- `\w` same as `[a-zA-Z0-9_]`
- `\W` same as `[^a-zA-Z0-9_]`
- `\a` ascii bell (BEL)
- `\b` ascii backspace (BS)
- `\f` ascii formfeed (FF)
- `\n` ascii linefeed (LF)
- `\r` ascii carriage return (CR)
- `\t` ascii horizontal tab (TAB)
- `\v` ascii vertical tab (VT)

numerical escape sequences:  
the positive integer number given will be converted to the associated character

- `\o` octal escape sequence, note: must be 3 digits long, this is different to the standard `\<octal_number>` to distinguish it from back references
- `\x` 8bit hexadecimal escape sequence, note: must be 2 digits long
- `\u` 16bit hexadecimal escape sequence, note: must be 4 digits long
- `\U` 32bit hexadecimal escape sequence, note: must be 8 digits long

all other escaped characters will be treated as themselves

`[]` sets

- the `^` modifier will include all ascii printable characters minus the specified ones
- the `-` range modifier will include all characters with integer values between and including the ranges specified

`()` groups (modifiers are not yet supported)

`|` or sequences, inside or outside groups

## Limitations

some features of regex do not make sense and will be ignored:

-   boundary assertion character (`^` and `$`)
-   all the beginning or end of word escape sequences
-   greedy and non greedy modifiers for counts (`+` and `?`),  
  maybe in future they could be used to set the generation order

limits by design, they may be supported if there is a reason to

-   unlimited counts such as `*` `+`  
  this is because i feel that generating an infinitely long string is mostly useless and it would complicate the parsing process more abstract and less easily serializable,  
  you are welcome to convince me otherwise.
-   group modifiers  
  is there a point for those for our scope?


## See also

inspired by: [janstarke/rexgen](https://github.com/janstarke/rexgen)  
friends: [Buba98/regex_enumerator](https://github.com/Buba98/regex_enumerator) (yes we know each other)

## License

`regenx` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
