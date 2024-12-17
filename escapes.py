import string

ascii_printable_set = set(string.printable)
ascii_printable = "".join(sorted(string.printable))

escapes = {
    "a": "\a",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "v": "\v",
    "d": "".join(sorted(string.digits)),
    "s": "".join(sorted(string.whitespace)),
    "w": "".join(sorted(string.ascii_letters + string.digits + "_")),
}
escapes.update({
    "D": "".join(sorted(ascii_printable_set - set(escapes["d"]))),
    "S": "".join(sorted(ascii_printable_set - set(escapes["s"]))),
    "W": "".join(sorted(ascii_printable_set - set(escapes["w"]))),
})
