import enum
import sys
from copy import deepcopy


class stable_set:
    def __init__(self, *args):
        self._dict = dict()
        self._count = 0
        for c in args:
            self.add(c)

    def add(self, c):
        self._dict[c] = self._count
        self._count += 1

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        return iter(self._dict)

    def __contains__(self, c):
        return c in self._dict

    def index(self, c):
        return self._dict[c]

    def __repr__(self):
        return "<" + repr(list(self._dict))[1:-1] + ">"


class State(enum.IntEnum):
    NONE = enum.auto()
    ESCAPE = enum.auto()
    SET = enum.auto()
    COUNT = enum.auto()
    GROUP = enum.auto()


def rmap(f, it):
    return (f(rmap(f, x)) if not isinstance(x, str) else x for x in it)


def parse(rule, i=0, states=None, previous_states=None, options=None):
    if options is None:
        options = []
    if previous_states is None:
        previous_states = []
    if states is None:
        states = [[State.NONE, len(options) - 1]]
    while i < len(rule):
        match states[-1][0]:
            case State.NONE:
                if rule[i] == "\\":  # escape sequence
                    states.append([State.ESCAPE, len(options)])
                elif rule[i] == "[":  # new set
                    options.append(stable_set())
                    states.append([State.SET, len(options)])
                elif rule[i] == "*" or rule[i] == "+":
                    raise SyntaxError(f"Invalid count, even if regex allows unlimited count max it's not possible to handle it for generation, error at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^")
                elif rule[i] == "?":  # new optional (same as count 0-1)
                    if len(options) > 0:
                        options.append([[options.pop()], ""])  # handled inline for speed and semplicity
                    else:
                        print(f"optional modifier character {rule[i]!r} applied to nothing, ignoring it, warning at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^", file=sys.stderr)
                    states.append([State.NONE, len(options)])
                elif rule[i] == "{":  # new count
                    count_values = [""]
                    states.append([State.COUNT, len(options)])
                elif rule[i] == "(":  # new group
                    options.append(stable_set())
                    states.append([State.GROUP, len(options)])
                elif rule[i] == "^" or rule[i] == "$":  # special char
                    print(f"boundary assertion character {rule[i]!r} is valid in regex  but does not make sense here, ignoring it, warning at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^", file=sys.stderr)
                else:  # normal char
                    options.append(stable_set())
                    options[-1].add(rule[i])
                    previous_states.append([State.NONE, len(options)])
            case State.ESCAPE:
                if states[-2][0] != State.SET:
                    options.append(stable_set())  # do not create a new option if escaping inside a set
                options[-1].add(rule[i])
                previous_states.append(states.pop())
            case State.SET:
                if rule[i] == "]":  # end set
                    if len(options[-1]) == 0:  # discard empty set
                        options.pop()
                    previous_states.append(states.pop())
                elif rule[i] == "\\":  # escape sequence in set
                    states.append([State.ESCAPE, len(options)])
                else:  # set opening char is allowed in set as a normal char
                    options[-1].add(rule[i])
            case State.COUNT:
                if rule[i] == "}":  # end count
                    assert 1 <= len(count_values) <= 2  # count only allows 1 or 2 arguments
                    if len(count_values) == 1:  # count with one argument
                        if len(count_values[0]) == 0:  # if no argument was given
                            raise SyntaxError(f"Invalid count, no count arguments given at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^")
                        min, max = 0, int(count_values[0])
                    else:  # count with two arguments
                        if len(count_values[1]) == 0:  # first argument is infinity by default if not given, but we can't do that
                            raise SyntaxError(f"Invalid count, even if regex allows unlimited count max it's not possible to handle it for generation, error at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^")
                        if len(count_values[0]) == 0:  # first argument is zero by default if not given
                            count_values[0] = 0
                        min, max = int(count_values[0]), int(count_values[1])
                    if min > max:  # the first count argument must be less than the second
                        raise SyntaxError(f"Invalid count, the first count argument must be less than the second at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^")
                    if max == 0:
                        options.pop()  # discard empty count
                    else:
                        # TODO: generate differently to remove duplicates (ex.: 'a', 'a' on "a?a?")
                        # TODO: generate differently to remove duplication of already optionals (ex.: '', '' on "a??")
                        options.append([[options.pop()]])
                        if min > 0:
                            for _ in range(1, min):
                                options[-1][-1].append(options[-1][-1][-1])
                            if max > 1 and max > min:
                                options[-1][-1].append(deepcopy(options[-1][-1][-1]))
                                options[-1][-1][-1].add("")
                        else:
                            options[-1][-1][-1].add("")
                        for _ in range(min + 1, max):
                            options[-1][-1].append(options[-1][-1][-1])
                    previous_states.append(states.pop())
                elif rule[i] == ",":  # next count argument
                    if len(count_values) >= 2:  # count only allows a max of 2 arguments
                        raise SyntaxError(f"Invalid count, too many count arguments at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^")
                    count_values.append("")
                elif rule[i] not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", }:
                    raise SyntaxError(f"Invalid count, invalid argument character at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^")
                else:
                    count_values[-1] += rule[i]
            case State.GROUP:
                if rule[i] == ")":
                    previous_states.append(states.pop())
        i += 1
    if states[-1][0] != State.NONE:
        raise SyntaxError(f"Invalid count, end of spec while still processing an open {states[-1][0].name} at index {i-1}: {rule[i-1]!r}\n\t{rule}\n\t{'~' * (i-1)}^")
    return list(rmap(list, options))


def r_or_gen(options, generated=""):
    # print("or in", options, generated)
    if isinstance(options, str):
        # print("or yeld str", options, generated, generated + options)
        yield generated + options
        return
    for o in options:
        for g in r_and_gen(o, generated=generated):
            # print("or yeld g", options, generated, g)
            yield g
    # print("or return", options, generated)


def r_and_gen(options, i=0, generated=""):
    # print("and in", options, i, generated)
    if isinstance(options, str):
        # print("or yeld str", options, i, generated, generated + options)
        yield generated + options
        return
    if i >= len(options):
        if i > 0:
            # print("and yeld i>0", options, i, generated)
            yield generated
        # print("and return i >= len(options)", options, i, generated)
        return
    for o in r_or_gen(options[i], generated=generated):
        for g in r_and_gen(options, i + 1, o):
            # print("and yeld g", options, i, generated, g)
            yield g
    # print("and return", options, i, generated)


def gen(options):
    # print("-" * 25)
    for r in r_and_gen(options):
        yield r
    # print("-" * 25)
