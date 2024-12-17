# RGen

_RGen_ is yet another regex based text generation library

## Features

This library currently supports generating all the possible strings that would match the given regex.

### Supported syntax

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

`()` groups (modifiers are not yet supported)

`|` or sequences, inside or outside groups
