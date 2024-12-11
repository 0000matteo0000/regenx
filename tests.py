from gen_pass import gen, parse

# BASE
assert (p := parse("")) == [], ["empty spec", p, "fail"]
assert (g := list(gen(p))) == [], ["empty spec", g, "fail"]
assert (p := parse("a")) == [["a"]], ["letter spec", p, "fail"]
assert (g := list(gen(p))) == ["a"], ["letter spec", g, "fail"]
assert (p := parse("abc")) == [["a"], ["b"], ["c"]], ["multiple letters spec", p, "fail"]
assert (g := list(gen(p))) == ["abc"], ["multiple letters spec", g, "fail"]
# IGNORED
assert (p := parse("^")) == [], ["start boundary assertion char spec", p, "fail"]
assert (g := list(gen(p))) == [], ["start boundary assertion char spec", g, "fail"]
assert (p := parse("$")) == [], ["end boundary assertion char spec", p, "fail"]
assert (g := list(gen(p))) == [], ["end boundary assertion char spec", g, "fail"]
# ESCAPE
assert (p := parse("\\a")) == [["a"]], ["escaped letter spec", p, "fail"]
assert (g := list(gen(p))) == ["a"], ["escaped letter spec", g, "fail"]
assert (p := parse("\\\\a")) == [["\\"], ["a"]], ["escaped escape char spec", p, "fail"]
assert (g := list(gen(p))) == ["\\a"], ["escaped escape char spec", g, "fail"]
assert (p := parse("\\a\\b\\c")) == [["a"], ["b"], ["c"]], ["multiple escaped letter spec", p, "fail"]
assert (g := list(gen(p))) == ["abc"], ["multiple escaped letter spec", g, "fail"]
assert (p := parse("\\\\a\\\\b\\\\c")) == [["\\"], ["a"], ["\\"], ["b"], ["\\"], ["c"]], ["multiple escaped escape char mixed with multiple letters spec", p, "fail"]
assert (g := list(gen(p))) == ["\\a\\b\\c"], ["multiple escaped escape char mixed with multiple letters spec", g, "fail"]
# SET
assert (p := parse("[]")) == [], ["empty set spec", p, "fail"]
assert (g := list(gen(p))) == [], ["empty set spec", g, "fail"]
assert (p := parse("[a]")) == [["a"]], ["single letter set spec", p, "fail"]
assert (g := list(gen(p))) == ["a"], ["single letter set spec", g, "fail"]
assert (p := parse("[abc]")) == [["a", "b", "c"]], ["multiple letters set spec", p, "fail"]
assert (g := list(gen(p))) == ["a", "b", "c"], ["multiple letters set spec", g, "fail"]
assert (p := parse("[a\\bc]")) == [["a", "b", "c"]], ["escaped letter set spec", p, "fail"]
assert (g := list(gen(p))) == ["a", "b", "c"], ["escaped letter set spec", g, "fail"]
assert (p := parse("[\\\\]")) == [["\\"]], ["escaped escape char set spec", p, "fail"]
assert (g := list(gen(p))) == ["\\"], ["escaped escape char set spec", g, "fail"]
assert (p := parse("[a\\\\c]")) == [["a", "\\", "c"]], ["escaped escape char set mixed with multiple letters spec", p, "fail"]
assert (g := list(gen(p))) == ["a", "\\", "c"], ["escaped escape char set mixed with multiple letters spec", g, "fail"]
assert (p := parse("[[]")) == [["["]], ["open set char spec", p, "fail"]
assert (g := list(gen(p))) == ["["], ["open set char spec", g, "fail"]
assert (p := parse("[\\[]")) == [["["]], ["escaped open set char spec", p, "fail"]
assert (g := list(gen(p))) == ["["], ["escaped open set char spec", g, "fail"]
assert (p := parse("[a[c]")) == [["a", "[", "c"]], ["open set char spec mixed with multiple letters spec", p, "fail"]
assert (g := list(gen(p))) == ["a", "[", "c"], ["open set char spec mixed with multiple letters spec", g, "fail"]
assert (p := parse("[a\\[c]")) == [["a", "[", "c"]], ["escaped open set char spec mixed with multiple letters spec", p, "fail"]
assert (g := list(gen(p))) == ["a", "[", "c"], ["escaped open set char spec mixed with multiple letters spec", g, "fail"]
assert (p := parse("[]]")) == [["]"]], ["empty set with close set char spec", p, "fail"]
assert (g := list(gen(p))) == ["]"], ["empty set with close set char spec", g, "fail"]
assert (p := parse("[\\]]")) == [["]"]], ["escaped close set char spec", p, "fail"]
assert (g := list(gen(p))) == ["]"], ["escaped close set char spec", g, "fail"]
assert (p := parse("[a]c]")) == [["a"], ["c"], ["]"]], ["close set char spec mixed with multiple letters spec", p, "fail"]
assert (g := list(gen(p))) == ["ac]"], ["close set char spec mixed with multiple letters spec", g, "fail"]
assert (p := parse("[a\\]c]")) == [["a", "]", "c"]], ["escaped close set char spec mixed with multiple letters spec", p, "fail"]
assert (g := list(gen(p))) == ["a", "]", "c"], ["escaped close set char spec mixed with multiple letters spec", g, "fail"]
# COUNT
exc = None
try:
    assert (p := parse("a{}")) == [], ["no count arguments syntax error", p, "fail"]
except SyntaxError as e:
    exc = e
exc = None
try:
    assert (p := parse("a{,,}")) == [], ["too many count arguments syntax error", p, "fail"]
except SyntaxError as e:
    exc = e
assert exc is not None, ["too many count arguments syntax error"]
exc = None
try:
    assert (p := parse("a{a,}")) == [], ["bad int in count arguments syntax error", p, "fail"]
except SyntaxError as e:
    exc = e
assert exc is not None, ["bad int in count arguments syntax error"]
exc = None
try:
    assert (p := parse("a{,a}")) == [], ["bad int in count arguments syntax error", p, "fail"]
except SyntaxError as e:
    exc = e
assert exc is not None, ["bad int in count arguments syntax error"]
exc = None
try:
    assert (p := parse("a{1,0}")) == [], ["bad min max count arguments order syntax error", p, "fail"]
except SyntaxError as e:
    exc = e
assert exc is not None, ["bad min max count arguments order syntax error"]
exc = None
try:
    assert (p := parse("a{,}")) == [], ["unbound count >=0 syntax error", p, "fail"]
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count >=0 syntax error"]
exc = None
try:
    assert (p := parse("a{1,}")) == [], ["unbound count >0 syntax error", p, "fail"]
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count >0 syntax error"]
assert (p := parse("a{0}")) == [], ["count with letter and single argument = 0 spec", p, "fail"]
assert (g := list(gen(p))) == [], ["count with letter and single argument = 0 spec", g, "fail"]
assert (p := parse("a{0,0}")) == [], ["count with letter and double argument = 0, 0 spec", p, "fail"]
assert (g := list(gen(p))) == [], ["count with letter and double argument = 0, 0 spec", g, "fail"]
assert (p := parse("a{1}")) == [[[["a", ""]]]], ["count with letter and single argument = 1 spec", p, "fail"]
assert (g := list(gen(p))) == ["a", ""], ["count with letter and single argument = 1 spec", g, "fail"]
assert (p := parse("a{0,1}")) == [[[["a", ""]]]], ["count with letter and double argument = 0, 1 spec", p, "fail"]
assert (g := list(gen(p))) == ["a", ""], ["count with letter and double argument = 0, 1 spec", g, "fail"]
assert (p := parse("a{1,1}")) == [[[["a"]]]], ["count with letter and double argument = 1, 1 spec", p, "fail"]
assert (g := list(gen(p))) == ["a"], ["count with letter and double argument = 1, 1 spec", g, "fail"]
assert (p := parse("a{2}")) == [[[["a", ""], ["a", ""]]]], ["count with letter and single argument >1 spec", p, "fail"]
assert (g := list(gen(p))) == ["aa", "a", "a", ""], ["count with letter and single argument >1 spec", g, "fail"]
assert (p := parse("a{0,2}")) == [[[["a", ""], ["a", ""]]]], ["count with letter and double argument 0, >1 spec", p, "fail"]  # should change
assert (g := list(gen(p))) == ["aa", "a", "a", ""], ["count with letter and double argument 0, >1 spec", g, "fail"]  # should change
assert (p := parse("a{1,2}")) == [[[["a"], ["a", ""]]]], ["count with letter and double argument 1, >1 spec", p, "fail"]
assert (g := list(gen(p))) == ["aa", "a"], ["count with letter and double argument 1, >1 spec", g, "fail"]
assert (p := parse("a{2,2}")) == [[[["a"], ["a"]]]], ["count with letter and double equal argument >1, >1 spec", p, "fail"]
assert (g := list(gen(p))) == ["aa"], ["count with letter and double equal argument >1, >1 spec", g, "fail"]
assert (p := parse("a{2,3}")) == [[[["a"], ["a"], ["a", ""]]]], ["count with letter and double different argument >1, >1 spec", p, "fail"]
assert (g := list(gen(p))) == ["aaa", "aa"], ["count with letter and double different argument >1, >1 spec", g, "fail"]
assert (p := parse("a{2,4}")) == [[[["a"], ["a"], ["a", ""], ["a", ""]]]], ["count with letter and double different argument >1, >1 spec", p, "fail"]  # should change
assert (g := list(gen(p))) == ["aaaa", "aaa", "aaa", "aa"], ["count with letter and double different argument >1, >1 spec", g, "fail"]  # should change
assert (p := parse("[a]{1}")) == [[[["a", ""]]]], ["count with single letter set and single argument = 1 spec", p, "fail"]
assert (g := list(gen(p))) == ["a", ""], ["count with single letter set and single argument = 1 spec", g, "fail"]
assert (p := parse("[ab]{1,2}")) == [[[["a", "b"], ["a", "b", ""]]]], ["count with multiple letters set and double argument 1, >1 spec", p, "fail"]
assert (g := list(gen(p))) == ["aa", "ab", "a", "ba", "bb", "b"], ["count with multiple letters set and double argument 1, >1 spec", g, "fail"]
exc = None
try:
    assert (p := parse("a*")) == [], ["unbound count *(>=0) syntax error", p, "fail"]
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count *(>=0) syntax error"]
exc = None
try:
    assert (p := parse("a+")) == [], ["unbound count +(>0) syntax error", p, "fail"]
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count +(>0) syntax error"]
assert (p := parse("a?")) == [[[["a"]], ""]], ["optional modifier with letter spec", p, "fail"]
assert (g := list(gen(p))) == ["a", ""], ["optional modifier with letter spec", g, "fail"]
assert (p := parse("a?b?")) == [[[["a"]], ""], [[["b"]], ""]], ["multiple optional modifier with letter spec", p, "fail"]
assert (g := list(gen(p))) == ["ab", "a", "b", ""], ["multiple optional modifier with letter spec", g, "fail"]
assert (p := parse("a??")) == [[[[[["a"]], ""]], ""]], ["duplicated optional modifier with letter spec", p, "fail"]  # should change
assert (g := list(gen(p))) == ["a", "", ""], ["duplicated optional modifier with letter spec", g, "fail"]  # should change
assert (p := parse("[a]?")) == [[[["a"]], ""]], ["optional modifier with single letter set spec", p, "fail"]
assert (g := list(gen(p))) == ["a", ""], ["optional modifier with single letter set spec", g, "fail"]
assert (p := parse("[abc]?")) == [[[["a", "b", "c"]], ""]], ["optional modifier with multiple letters set spec", p, "fail"]
assert (g := list(gen(p))) == ["a", "b", "c", ""], ["optional modifier with multiple letters set spec", g, "fail"]
assert (p := parse("a{0,1}?")) == [[[[[["a", ""]]]], ""]], ["optional modifier with count with letter and double argument = 0, 1 spec", p, "fail"]  # should change
assert (g := list(gen(p))) == ["a", "", ""], ["optional modifier with count with letter and double argument = 0, 1 spec", g, "fail"]  # should change
assert (p := parse("a{1,1}?")) == [[[[[["a"]]]], ""]], ["optional modifier with count with letter and double argument = 1, 1 spec", p, "fail"]  # should change
assert (g := list(gen(p))) == ["a", ""], ["optional modifier with count with letter and double argument = 1, 1 spec", g, "fail"]    # should change
assert (p := parse("[a]{1}?")) == [[[[[["a", ""]]]], ""]], ["optional modifier with count with single letter set and single argument = 1 spec", p, "fail"]  # should change
assert (g := list(gen(p))) == ["a", "", ""], ["optional modifier with count with single letter set and single argument = 1 spec", g, "fail"]  # should change
assert (p := parse("[ab]{1,2}?")) == [[[[[["a", "b"], ["a", "b", ""]]]], ""]], ["optional modifier with count with multiple letters set and double argument 1, >1 spec", p, "fail"]
assert (g := list(gen(p))) == ["aa", "ab", "a", "ba", "bb", "b", ""], ["optional modifier with count with multiple letters set and double argument 1, >1 spec", g, "fail"]
# consider testing for group count
# GROUP
