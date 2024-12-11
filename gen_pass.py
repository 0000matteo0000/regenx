import enum
import string
from copy import deepcopy
import sys


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
        return "<" + repr(list(self._dict)) + ">"


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
        states = [[State.NONE, len(options)]]
    while i < len(rule):
        match states[-1][0]:
            case State.NONE:
                if rule[i] == "\\":  # escape sequence
                    states.append([State.ESCAPE, len(options)])
                elif rule[i] == "[":  # new set
                    options.append(stable_set())
                    states.append([State.SET, len(options)])
                elif rule[i] in "*+":
                    raise SyntaxError(f"Invalid count, even if regex allows unlimited count max it's not possible to handle it for generation, error at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^")
                elif rule[i] in "?":  # new optional (same as count 0-1)
                    print(rule, i, options, states[-1])
                    print(list(range(len(options)-1, states[-1][1]-1, -1)))
                    options.append([[options.pop(j) for j in range(len(options)-1, states[-1][1]-1, -1)], ""])  # handled inline for speed and semplicity
                    print(rule, i, options, states[-1])
                elif rule[i] == "{":  # new count
                    states.append([State.COUNT, len(options)])
                    count_values = [""]
                elif rule[i] == "(":  # new group
                    options.append(stable_set())
                    states.append([State.GROUP, len(options)])
                elif rule[i] == "^" or rule[i] == "$":  # special char
                    print(f"boundary assertion character {rule[i]!r} is valid in regex  but does not make sense here, ignoring it, warning at index {i}: {rule[i]!r}\n\t{rule}\n\t{'~' * i}^", file=sys.stderr)
                else:  # normal char
                    options.append(stable_set())
                    options[-1].add(rule[i])
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
                        if min > 0:
                            for _ in range(1, min):
                                options.append(options[-1])
                            if max > 1 and max > min:
                                options.append(deepcopy(options[-1]))
                                options[-1].add("")
                        else:
                            options[-1].add("")
                        for _ in range(min + 1, max):
                            options.append(options[-1])
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


def rgen(options, i=0, generated="", generateds=None):
    if i >= len(options):
        if i > 0:
            yield generated
        return
    if generateds is None:
        generateds = []
    generateds.append(None)
    for o in options[i]:
        if len(generateds) > 1 and generateds[-2] == "" and "" in options[i] and o != "":  # skip duplicated generations
            continue
        generateds[-1] = o
        for r in rgen(options, i + 1, generated + o, generateds):
            yield r
    generateds.pop()


def gen(options):
    for r in rgen(options):
        yield r


# BASE
assert (p := parse("")) == [], ["empty spec", p]
assert (g := list(gen(p))) == [], ["empty spec", g]
assert (p := parse("a")) == [["a", ],], ["letter spec", p]
assert (g := list(gen(p))) == ["a",], ["letter spec", g]
assert (p := parse("abc")) == [["a", ], ["b", ], ["c", ],], ["multiple letters spec", p]
assert (g := list(gen(p))) == ["abc",], ["multiple letters spec", g]
# IGNORED
assert (p := parse("^")) == [], ["start boundary assertion char spec", p]
assert (g := list(gen(p))) == [], ["start boundary assertion char spec", g]
assert (p := parse("$")) == [], ["end boundary assertion char spec", p]
assert (g := list(gen(p))) == [], ["end boundary assertion char spec", g]
# ESCAPE
assert (p := parse("\\a")) == [["a", ],], ["escaped letter spec", p]
assert (g := list(gen(p))) == ["a",], ["escaped letter spec", g]
assert (p := parse("\\\\a")) == [["\\", ], ["a", ],], ["escaped escape char spec", p]
assert (g := list(gen(p))) == ["\\a",], ["escaped escape char spec", g]
assert (p := parse("\\a\\b\\c")) == [["a", ], ["b", ], ["c", ],], ["multiple escaped letter spec", p]
assert (g := list(gen(p))) == ["abc",], ["multiple escaped letter spec", g]
assert (p := parse("\\\\a\\\\b\\\\c")) == [["\\", ], ["a", ], ["\\", ], ["b", ], ["\\", ], ["c", ],], ["multiple escaped escape char mixed with multiple letters spec", p]
assert (g := list(gen(p))) == ["\\a\\b\\c",], ["multiple escaped escape char mixed with multiple letters spec", g]
# SET
assert (p := parse("[]")) == [], ["empty set spec", p]
assert (g := list(gen(p))) == [], ["empty set spec", g]
assert (p := parse("[a]")) == [["a", ],], ["single letter set spec", p]
assert (g := list(gen(p))) == ["a",], ["single letter set spec", g]
assert (p := parse("[abc]")) == [["a", "b", "c"],], ["multiple letters set spec", p]
assert (g := list(gen(p))) == ["a", "b", "c",], ["multiple letters set spec", g]
assert (p := parse("[a\\bc]")) == [["a", "b", "c"],], ["escaped letter set spec", p]
assert (g := list(gen(p))) == ["a", "b", "c",], ["escaped letter set spec", g]
assert (p := parse("[\\\\]")) == [["\\", ],], ["escaped escape char set spec", p]
assert (g := list(gen(p))) == ["\\",], ["escaped escape char set spec", g]
assert (p := parse("[a\\\\c]")) == [["a", "\\", "c"],], ["escaped escape char set mixed with multiple letters spec", p]
assert (g := list(gen(p))) == ["a", "\\", "c",], ["escaped escape char set mixed with multiple letters spec", g]
assert (p := parse("[[]")) == [["[",],], ["open set char spec", p]
assert (g := list(gen(p))) == ["[",], ["open set char spec", g]
assert (p := parse("[\\[]")) == [["[",],], ["escaped open set char spec", p]
assert (g := list(gen(p))) == ["[",], ["escaped open set char spec", g]
assert (p := parse("[a[c]")) == [["a", "[", "c"],], ["open set char spec mixed with multiple letters spec", p]
assert (g := list(gen(p))) == ["a", "[", "c",], ["open set char spec mixed with multiple letters spec", g]
assert (p := parse("[a\\[c]")) == [["a", "[", "c"],], ["escaped open set char spec mixed with multiple letters spec", p]
assert (g := list(gen(p))) == ["a", "[", "c",], ["escaped open set char spec mixed with multiple letters spec", g]
assert (p := parse("[]]")) == [["]",],], ["empty set with close set char spec", p]
assert (g := list(gen(p))) == ["]",], ["empty set with close set char spec", g]
assert (p := parse("[\\]]")) == [["]",],], ["escaped close set char spec", p]
assert (g := list(gen(p))) == ["]",], ["escaped close set char spec", g]
assert (p := parse("[a]c]")) == [["a",], ["c",], ["]",],], ["close set char spec mixed with multiple letters spec", p]
assert (g := list(gen(p))) == ["ac]",], ["close set char spec mixed with multiple letters spec", g]
assert (p := parse("[a\\]c]")) == [["a", "]", "c"],], ["escaped close set char spec mixed with multiple letters spec", p]
assert (g := list(gen(p))) == ["a", "]", "c",], ["escaped close set char spec mixed with multiple letters spec", g]
# COUNT
exc = None
try:
    assert (p := parse("a{}")) == [], ["no count arguments syntax error", p]
except SyntaxError as e:
    exc = e
exc = None
try:
    assert (p := parse("a{,,}")) == [], ["too many count arguments syntax error", p]
except SyntaxError as e:
    exc = e
assert exc is not None, ["too many count arguments syntax error"]
exc = None
try:
    assert (p := parse("a{a,}")) == [], ["bad int in count arguments syntax error", p]
except SyntaxError as e:
    exc = e
assert exc is not None, ["bad int in count arguments syntax error"]
exc = None
try:
    assert (p := parse("a{,a}")) == [], ["bad int in count arguments syntax error", p]
except SyntaxError as e:
    exc = e
assert exc is not None, ["bad int in count arguments syntax error"]
exc = None
try:
    assert (p := parse("a{1,0}")) == [], ["bad min max count arguments order syntax error", p]
except SyntaxError as e:
    exc = e
assert exc is not None, ["bad min max count arguments order syntax error"]
exc = None
try:
    assert (p := parse("a{,}")) == [], ["unbound count >=0 syntax error", p]
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count >=0 syntax error"]
exc = None
try:
    assert (p := parse("a{1,}")) == [], ["unbound count >0 syntax error", p]
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count >0 syntax error"]
assert (p := parse("a{0}")) == [], ["count with letter and single argument = 0 spec", p]
assert (g := list(gen(p))) == [], ["count with letter and single argument = 0 spec", g]
assert (p := parse("a{0,0}")) == [], ["count with letter and double argument = 0, 0 spec", p]
assert (g := list(gen(p))) == [], ["count with letter and double argument = 0, 0 spec", g]
assert (p := parse("a{1}")) == [["a", "",], ], ["count with letter and single argument = 1 spec", p]
assert (g := list(gen(p))) == ["a", "",], ["count with letter and single argument = 1 spec", g]
assert (p := parse("a{0,1}")) == [["a", "",], ], ["count with letter and double argument = 0, 1 spec", p]
assert (g := list(gen(p))) == ["a", "",], ["count with letter and double argument = 0, 1 spec", g]
assert (p := parse("a{1,1}")) == [["a",], ], ["count with letter and double argument = 1, 1 spec", p]
assert (g := list(gen(p))) == ["a",], ["count with letter and double argument = 1, 1 spec", g]
assert (p := parse("a{2}")) == [["a", "",], ["a", "",],], ["count with letter and single argument >1 spec", p]
assert (g := list(gen(p))) == ["aa", "a", "",], ["count with letter and single argument >1 spec", g]
assert (p := parse("a{0,2}")) == [["a", "",], ["a", "",],], ["count with letter and double argument 0, >1 spec", p]
assert (g := list(gen(p))) == ["aa", "a", "",], ["count with letter and double argument 0, >1 spec", g]
assert (p := parse("a{1,2}")) == [["a",], ["a", "",],], ["count with letter and double argument 1, >1 spec", p]
assert (g := list(gen(p))) == ["aa", "a",], ["count with letter and double argument 1, >1 spec", g]
assert (p := parse("a{2,2}")) == [["a",], ["a",],], ["count with letter and double equal argument >1, >1 spec", p]
assert (g := list(gen(p))) == ["aa",], ["count with letter and double equal argument >1, >1 spec", g]
assert (p := parse("a{2,3}")) == [["a",], ["a",], ["a", "",],], ["count with letter and double different argument >1, >1 spec", p]
assert (g := list(gen(p))) == ["aaa", "aa",], ["count with letter and double different argument >1, >1 spec", g]
assert (p := parse("a{2,4}")) == [["a",], ["a",], ["a", "",], ["a", "",],], ["count with letter and double different argument >1, >1 spec", p]
assert (g := list(gen(p))) == ["aaaa", "aaa", "aa",], ["count with letter and double different argument >1, >1 spec", g]
exc = None
try:
    assert (p := parse("a*")) == [], ["unbound count *(>=0) syntax error", p]
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count *(>=0) syntax error"]
exc = None
try:
    assert (p := parse("a+")) == [], ["unbound count +(>0) syntax error", p]
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count +(>0) syntax error"]
assert (p := parse("a?")) == [[[["a",],], "",], ], ["optional count with letter spec", p]
assert (g := list(gen(p))) == ["a", "",], ["optional count with letter spec", g]
assert (p := parse("a??")) == [[["a"], "",], ], ["optional count with letter spec", p]
assert (g := list(gen(p))) == ["a", "",], ["optional count with letter spec", g]
assert (p := parse("a{1,1}?")) == [["a", "",],], ["-", p]
assert (g := list(gen(p))) == ["a", "",], ["-", g]
assert (p := parse("a{2,2}")) == [["a",], ["a",],], ["-", p]
assert (g := list(gen(p))) == ["aa",], ["-", g]
assert (p := parse("a{2,2}?")) == [[["a",], ["a"],], "",], ["-", p]  # this is broken ? should apply to the whole count
assert (g := list(gen(p))) == ["aa", "",], ["-", g]
# consider testing for set count
# consider testing for group count
# GROUP

if __name__ == "__main__":
    for i, rule in enumerate(sys.argv):
        if i == 0:
            continue
        print(i, rule, file=sys.stderr)
        for g in gen(parse(rule)):
            print(g)
