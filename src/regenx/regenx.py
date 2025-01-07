# SPDX-FileCopyrightText: 2024-present 0000matteo0000 <matteo.sid@hotmail.it>
#
# SPDX-License-Identifier: MIT

import enum
import logging
from copy import deepcopy

from regenx.escapes import ascii_printable, escapes

logger = logging.getLogger(__name__)
logging_format = "%(levelname)s:%(filename)s:%(funcName)s:%(message)s"
logging.basicConfig(encoding="utf-8", format=logging_format, level=logging.WARNING)

MAX_ASCII = 255


class StableSet:
    def __init__(self, *args):
        self.__dict = {}
        # self.__count = 0
        # self.__dirty_count = False
        for c in args:
            self.add(c)

    def add(self, c):
        if len(c) <= 1:
            self.__dict[c] = None  # self.__count
            # self.__count += 1
        else:
            for cc in c:
                self.__dict[cc] = None  # self.__count
                # self.__count += 1

    def remove(self, c):
        self.__dict.pop(c)
        # self.__dirty_count = True  # lazy index update
        # self.__count -= 1

    def __len__(self):
        return len(self.__dict)

    def __iter__(self):
        return iter(self.__dict)

    def __contains__(self, c):
        return c in self.__dict

    def __getitem__(self, i):
        return list(self.__dict.keys())[i]

    # def __recount(self):
    #     self.__count = 0
    #     for c in self.__dict:
    #         self.__dict[c] = self.__count
    #         self.__count += 1

    # def index(self, c):
    #     if self.__dirty_count:  # lazy index update
    #         self.__recount()
    #     return self.__dict[c]

    def __repr__(self):
        return "<" + repr(list(self.__dict))[1:-1] + ">"


class State(enum.IntEnum):
    NONE = enum.auto()
    ESCAPE = enum.auto()
    SET = enum.auto()
    COUNT = enum.auto()
    OR = enum.auto()
    GROUP = enum.auto()


def read_hex(rule, ii=0, n=2):
    values = ""
    for i in range(ii, ii + n):
        if i >= len(rule):
            logger.debug("SystaxError unclosed %r", State.ESCAPE)
            e = f"Invalid spec, end of spec while still processing an open {State.ESCAPE.name} at index {i-1}: {rule[i-1]!r}\n\t{rule}\n\t{'~' * (i-1)}^"
            raise SyntaxError(e)
        match rule[i]:
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f" | "A" | "B" | "C" | "D" | "E" | "F":
                logger.debug("case %r", rule[i])
                values += rule[i]
                logger.debug("values %r", values)
            case _:
                e = f"Invalid hexadecimal escape sequence, invalid hexadecimal character at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^"
                raise SyntaxError(e)
    return chr(int(values, 16)), i


def read_oct(rule, ii=0, n=3):
    values = ""
    for i in range(ii, ii + n):
        if i >= len(rule):
            logger.debug("SystaxError unclosed %r", State.ESCAPE)
            e = f"Invalid spec, end of spec while still processing an open {State.ESCAPE.name} at index {i-1}: {rule[i-1]!r}\n\t{rule}\n\t{'~' * (i-1)}^"
            raise SyntaxError(e)
        match rule[i]:
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7":
                logger.debug("case %r", rule[i])
                values += rule[i]
                logger.debug("values %r", values)
            case _:
                e = f"Invalid octal escape sequence, invalid octal character at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^"
                raise SyntaxError(e)
    ov = int(values, 8)
    if ov > MAX_ASCII:
        e = f"Invalid octal escape sequence, invalid octal value ({ov!r} is > than 255 = 0o377 = 0xff) at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^"
        raise SyntaxError(e)
    return chr(ov), i


def rparse_escape(rule, i=0, states=None, options=None):
    logger.debug("enter %r, %r, %r, %r", rule, i, states, options)
    # skip registering state since this function does not recurse
    if states[-1] != State.SET:
        options.append(StableSet())  # do not create a new option if escaping inside a set
        logger.debug("set %r %r", states[-1], State.SET)
    if i >= len(rule):
        logger.debug("SystaxError unclosed %r", State.ESCAPE)
        e = f"Invalid spec, end of spec while still processing an open {State.ESCAPE.name} at index {i-1}: {rule[i-1]!r}\n\t{rule}\n\t{'~' * (i-1)}^"
        raise SyntaxError(e)
    logger.debug("case %r", rule[i])
    if rule[i] in escapes:
        r = escapes[rule[i]]
    else:
        match rule[i]:
            case "x":
                r, i = read_hex(rule, ii=i + 1, n=2)
            case "o":
                r, i = read_oct(rule, ii=i + 1, n=3)
            case "u":
                r, i = read_hex(rule, ii=i + 1, n=4)
            case "U":
                r, i = read_hex(rule, ii=i + 1, n=8)
            case _:
                r = rule[i]
    logger.debug("r %r", r)
    options[-1].add(r)
    logger.debug("options %r", options[-1])
    logger.debug("return %r, %r", i, options)
    return i, options


def rparse_set(rule, i=0, states=None, options=None):
    logger.debug("se_setenter %r, %r, %r, %r", rule, i, states, options)
    negative_group = False
    if i >= len(rule):
        logger.debug("SystaxError unclosed %r", State.SET)
        e = f"Invalid spec, end of spec while still processing an open {State.SET.name} at index {i-1}: {rule[i-1]!r}\n\t{rule}\n\t{'~' * (i-1)}^"
        raise SyntaxError(e)
    if rule[i] == "^":
        logger.debug("negative %r", rule[i])
        negative_group = True
        i += 1
        if i >= len(rule):
            logger.debug("SystaxError unclosed %r", State.SET)
            e = f"Invalid spec, end of spec while still processing an open {State.SET.name} at index {i-1}: {rule[i-1]!r}\n\t{rule}\n\t{'~' * (i-1)}^"
            raise SyntaxError(e)
    if not negative_group:
        options.append(StableSet())
    else:
        options.append(StableSet(ascii_printable))
    logger.debug("options %r", options[-1])
    while i < len(rule):
        match rule[i]:
            case "]":  # end set
                logger.debug("case %r", rule[i])
                logger.debug("options %r", options[-1])
                if len(options[-1]) == 0:  # discard empty set
                    logger.debug("options pop empty")
                    options.pop()
                logger.debug("return %r, %r", i, options)
                return i, options
            case "\\":  # escape sequence in set
                logger.debug("case %r", rule[i])
                states.append(State.SET)
                i, options = rparse_escape(rule, i=i + 1, states=states, options=options)
                states.pop()
            case "-":  # escape sequence in set
                logger.debug("case %r", rule[i])
                i += 1
                if i >= len(rule):
                    logger.debug("SystaxError unclosed %r", State.SET)
                    e = f"Invalid spec, end of spec while still processing an open {State.SET.name} at index {i-1}: {rule[i-1]!r}\n\t{rule}\n\t{'~' * (i-1)}^"
                    raise SyntaxError(e)
                s, e = ord(options[-1][-1]), ord(rule[i])
                d = 1 if s < e else -1
                for r in map(chr, range(s + d, e + d, d)):
                    if not negative_group:
                        options[-1].add(r)
                    else:
                        options[-1].remove(r)
                logger.debug("options %r", options[-1])
            case _:  # set opening char is allowed in set as a normal char
                logger.debug("case %r", rule[i])
                if not negative_group:
                    options[-1].add(rule[i])
                else:
                    options[-1].remove(rule[i])
                logger.debug("options %r", options[-1])
        i += 1
    logger.debug("SystaxError unclosed %r", State.SET)
    e = f"Invalid spec, end of spec while still processing an open {State.SET.name} at index {i-1}: {rule[i-1]!r}\n\t{rule}\n\t{'~' * (i-1)}^"
    raise SyntaxError(e)


def rparse_count(rule, i=0, states=None, options=None):
    logger.debug("enter %r, %r, %r, %r", rule, i, states, options)
    # skip registering state since this function does not recurse
    count_values = [""]
    while i < len(rule):
        match rule[i]:
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                logger.debug("case %r", rule[i])
                count_values[-1] += rule[i]
            case ",":  # next count argument
                logger.debug("case %r", rule[i])
                if len(count_values) >= 2:  # count only allows a max of 2 argumentsc  # noqa: PLR2004
                    e = f"Invalid count, too many count arguments at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^"
                    raise SyntaxError(e)
                count_values.append("")
            case "}":  # end count
                logger.debug("case %r", rule[i])
                assert 1 <= len(count_values) <= 2  # count only allows 1 or 2 arguments  # noqa: S101,PLR2004
                if len(count_values) == 1:  # count with one argument
                    if len(count_values[0]) == 0:  # if no argument was given
                        e = f"Invalid count, no count arguments given at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^"
                        raise SyntaxError(e)
                    max_ = int(count_values[0])
                    min_ = max_
                else:  # count with two arguments
                    if len(count_values[1]) == 0:  # first argument is infinity by default if not given, but we can't do that
                        e = f"Invalid count, even if regex allows unlimited count max it's not possible to handle it for generation, error at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^"
                        raise SyntaxError(e)
                    if len(count_values[0]) == 0:  # first argument is zero by default if not given
                        count_values[0] = 0
                    min_, max_ = int(count_values[0]), int(count_values[1])
                if min_ > max_:  # the first count argument must be less than the second
                    e = f"Invalid count, the first count argument must be less than the second at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^"
                    raise SyntaxError(e)
                if max_ == 0:
                    logger.debug("options pop empty")
                    options.pop()  # discard empty count
                else:
                    # TODO: generate differently to remove duplicates (ex.: 'a', 'a' on "a?a?")
                    # TODO: generate differently to remove duplication of already optionals (ex.: '', '' on "a??")
                    options.append([[options.pop()]])
                    if min_ > 0:
                        for _ in range(1, min_):
                            options[-1][-1].append(options[-1][-1][-1])
                        if max_ > 1 and max_ > min_:
                            options[-1][-1].append(deepcopy(options[-1][-1][-1]))
                            options[-1][-1][-1].add("")
                    else:
                        options[-1][-1][-1].add("")
                    for _ in range(min_ + 1, max_):
                        options[-1][-1].append(options[-1][-1][-1])
                logger.debug("return %r, %r", i, options)
                return i, options
            case _:
                logger.debug("case %r", rule[i])
                e = f"Invalid count, invalid argument character at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^"
                raise SyntaxError(e)
        i += 1
    logger.debug("SystaxError unclosed %r", State.COUNT)
    e = f"Invalid spec, end of spec while still processing an open {State.COUNT.name} at index {i-1}: {rule[i-1]!r}\n\t{rule}\n\t{'~' * (i-1)}^"
    raise SyntaxError(e)


def rparse(rule, i=0, states=None, options=None):
    if options is None:
        options = []
    if states is None:
        states = [State.NONE]
    enter_state_index = len(states) - 1
    while i < len(rule):
        match rule[i]:
            case ".":  # any char
                logger.debug("case %r", rule[i])
                options.append(StableSet(ascii_printable))
            case "\\":  # escape sequence
                logger.debug("case %r", rule[i])
                i, options = rparse_escape(rule, i=i + 1, states=states, options=options)
            case "[":  # new set
                logger.debug("case %r", rule[i])
                i, options = rparse_set(rule, i=i + 1, states=states, options=options)
            case "*" | "+":
                logger.debug("case %r", rule[i])
                e = f"Invalid count, even if regex allows unlimited count max it's not possible to handle it for generation, error at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^"
                raise SyntaxError(e)
            case "{":  # new count
                logger.debug("case %r", rule[i])
                i, options = rparse_count(rule, i=i + 1, states=states, options=options)
            case "|":  # new or
                logger.debug("case %r", rule[i])
                if len(states) > 1 and states[enter_state_index] == State.OR:
                    if len(options) == 0:
                        options = [[""]]
                    return options, i
                states.append(State.OR)
                options = (
                    [
                        [
                            options,
                        ]
                    ]
                    if len(options) > 0
                    else [
                        [
                            [[""]],
                        ]
                    ]
                )
                while i < len(rule) and rule[i] == "|":
                    o, i = rparse(rule, i=i + 1, states=states)
                    options[-1].append(o)
                if i < len(rule) and rule[i] == ")":
                    i -= 1  # allow closing for the parent group too
                states.pop()
            case "(":  # new group
                logger.debug("case %r", rule[i])
                states.append(State.GROUP)
                o, i = rparse(rule, i=i + 1, states=states)
                options.append([o])
                states.pop()
            case ")":
                logger.debug("case %r", rule[i])
                if states[enter_state_index] == State.GROUP or (states[enter_state_index] == State.OR and enter_state_index > 0 and states[enter_state_index - 1] == State.GROUP):
                    if len(options) == 0:
                        options = [[""]]
                    return options, i
                e = f"Invalid spec, closing group that was never opened {rule[i]!r} at index {i-1}: {rule[i-1]!r}\n\t{rule}\n\t{'~' * (i-1)}^"
                raise SyntaxError(e)
            case "^" | "$":  # special char
                logger.debug("case %r", rule[i])
                w = f"boundary assertion character {rule[i]!r} is valid in regex  but does not make sense here, ignoring it, warning at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^"
                logger.warning(w)
            case _:  # normal char
                logger.debug("case %r", rule[i])
                options.append(StableSet())
                options[-1].add(rule[i])
        i += 1
    if states[-1] != State.NONE and states[-1] != State.OR:
        logger.debug("SystaxError unclosed %r", states[-1])
        e = f"Invalid spec, end of spec while still processing an open {states[-1].name} at index {i-1}: {rule[i-1]!r}\n\t{rule}\n\t{'~' * (i-1)}^"
        raise SyntaxError(e)
    if len(options) == 0:
        options = [[""]]
    logger.debug("return %r, %r", i, options)
    return options, i


def rmap(f, it):
    return (f(rmap(f, x)) if not isinstance(x, str) else x for x in it)


def parse(rule, i=0, states=None, options=None):
    logger.debug("-" * 25)
    logger.info("enter %r, %r, %r, %r", rule, i, states, options)
    p = list(rmap(list, rparse(rule, i=i, states=states, options=options)[0]))
    logger.debug("-" * 25)
    return p


def r_or_gen(options, generated=""):
    logger.debug("in %r, %r", options, generated)
    if isinstance(options, str):
        logger.debug("yeld str %r, %r, %r", options, generated, generated + options)
        yield generated + options
        return
    for o in options:
        for g in r_and_gen(o, generated=generated):
            logger.debug("yeld g %r, %r, %r", options, generated, g)
            yield g
    logger.debug("return %r, %r", options, generated)


def r_and_gen(options, i=0, generated=""):
    logger.debug("in %r, %r, %r", options, i, generated)
    if isinstance(options, str):
        logger.debug("yeld str %r, %r, %r, %r", options, i, generated, generated + options)
        yield generated + options
        return
    if i >= len(options):
        if i > 0:
            logger.debug("yeld i>0 %r, %r, %r", options, i, generated)
            yield generated
        logger.debug("return i >= len(options) %r, %r, %r", options, i, generated)
        return
    for o in r_or_gen(options[i], generated=generated):
        for g in r_and_gen(options, i + 1, o):
            logger.debug("yeld g %r, %r, %r", options, generated, g)
            yield g
    logger.debug("return %r, %r, %r", options, i, generated)


def gen(options, count=None):
    logger.debug("-" * 25)
    for i, r in enumerate(r_and_gen(options)):
        if count is not None and i >= count:
            break
        yield r
    logger.debug("-" * 25)
