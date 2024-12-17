from gen_pass import gen, parse

# BASE
assert (p := parse(s := "")) == [[""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == [""], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a")) == [["a"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "abc")) == [["a"], ["b"], ["c"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["abc"], "".join(map(str, [repr(s), ": generation fail: ", g]))
# IGNORED
assert (p := parse(s := "^")) == [[""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == [""], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "$")) == [[""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == [""], "".join(map(str, [repr(s), ": generation fail: ", g]))
# ESCAPE
assert (p := parse(s := "\\a")) == [["a"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "\\\\a")) == [["\\"], ["a"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["\\a"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "\\a\\b\\c")) == [["a"], ["b"], ["c"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["abc"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "\\\\a\\\\b\\\\c")) == [["\\"], ["a"], ["\\"], ["b"], ["\\"], ["c"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["\\a\\b\\c"], "".join(map(str, [repr(s), ": generation fail: ", g]))
# SET
assert (p := parse(s := "[]")) == [[""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == [""], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[a]")) == [["a"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[abc]")) == [["a", "b", "c"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", "b", "c"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[a\\bc]")) == [["a", "b", "c"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", "b", "c"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[\\\\]")) == [["\\"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["\\"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[a\\\\c]")) == [["a", "\\", "c"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", "\\", "c"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[[]")) == [["["]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["["], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[\\[]")) == [["["]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["["], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[a[c]")) == [["a", "[", "c"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", "[", "c"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[a\\[c]")) == [["a", "[", "c"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", "[", "c"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[]]")) == [["]"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["]"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[\\]]")) == [["]"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["]"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[a]c]")) == [["a"], ["c"], ["]"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["ac]"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[a\\]c]")) == [["a", "]", "c"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", "]", "c"], "".join(map(str, [repr(s), ": generation fail: ", g]))
# COUNT
exc = None
try:
    assert (p := parse(s := "a{}")) == [], "".join(map(str, [repr(s), ":  parse fail: ", p]))
except SyntaxError as e:
    exc = e
exc = None
try:
    assert (p := parse(s := "a{,,}")) == [], "".join(map(str, [repr(s), ":  parse fail: ", p]))
except SyntaxError as e:
    exc = e
assert exc is not None, ["too many count arguments syntax error"]
exc = None
try:
    assert (p := parse(s := "a{a,}")) == [], "".join(map(str, [repr(s), ":  parse fail: ", p]))
except SyntaxError as e:
    exc = e
assert exc is not None, ["bad int in count arguments syntax error"]
exc = None
try:
    assert (p := parse(s := "a{,a}")) == [], "".join(map(str, [repr(s), ":  parse fail: ", p]))
except SyntaxError as e:
    exc = e
assert exc is not None, ["bad int in count arguments syntax error"]
exc = None
try:
    assert (p := parse(s := "a{1,0}")) == [], "".join(map(str, [repr(s), ":  parse fail: ", p]))
except SyntaxError as e:
    exc = e
assert exc is not None, ["bad min max count arguments order syntax error"]
exc = None
try:
    assert (p := parse(s := "a{,}")) == [], "".join(map(str, [repr(s), ":  parse fail: ", p]))
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count >=0 syntax error"]
exc = None
try:
    assert (p := parse(s := "a{1,}")) == [], "".join(map(str, [repr(s), ":  parse fail: ", p]))
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count >0 syntax error"]
assert (p := parse(s := "a{0}")) == [[""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == [""], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a{0,0}")) == [[""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == [""], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a{1}")) == [[[["a"]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a{0,1}")) == [[[["a", ""]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a{1,1}")) == [[[["a"]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a{2}")) == [[[["a"], ["a"]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["aa"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a{0,2}")) == [[[["a", ""], ["a", ""]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))  # should change
assert (g := list(gen(p))) == ["aa", "a", "a", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))  # should change
assert (p := parse(s := "a{1,2}")) == [[[["a"], ["a", ""]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["aa", "a"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a{2,2}")) == [[[["a"], ["a"]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["aa"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a{2,3}")) == [[[["a"], ["a"], ["a", ""]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["aaa", "aa"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a{2,4}")) == [[[["a"], ["a"], ["a", ""], ["a", ""]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))  # should change
assert (g := list(gen(p))) == ["aaaa", "aaa", "aaa", "aa"], "".join(map(str, [repr(s), ": generation fail: ", g]))  # should change
assert (p := parse(s := "[a]{1}")) == [[[["a"]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[ab]{1,2}")) == [[[["a", "b"], ["a", "b", ""]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["aa", "ab", "a", "ba", "bb", "b"], "".join(map(str, [repr(s), ": generation fail: ", g]))
exc = None
try:
    assert (p := parse(s := "a*")) == [], "".join(map(str, [repr(s), ":  parse fail: ", p]))
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count *(>=0) syntax error"]
exc = None
try:
    assert (p := parse(s := "a+")) == [], "".join(map(str, [repr(s), ":  parse fail: ", p]))
except SyntaxError as e:
    exc = e
assert exc is not None, ["unbound count +(>0) syntax error"]
assert (p := parse(s := "a?")) == [[[["a"]], ""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a?b?")) == [[[["a"]], ""], [[["b"]], ""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["ab", "a", "b", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a??")) == [[[[[["a"]], ""]], ""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))  # should change
assert (g := list(gen(p))) == ["a", "", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))  # should change
assert (p := parse(s := "[a]?")) == [[[["a"]], ""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "[abc]?")) == [[[["a", "b", "c"]], ""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", "b", "c", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a{0,1}?")) == [[[[[["a", ""]]]], ""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))  # should change
assert (g := list(gen(p))) == ["a", "", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))  # should change
assert (p := parse(s := "a{1,1}?")) == [[[[[["a"]]]], ""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))  # should change
assert (g := list(gen(p))) == ["a", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))    # should change
assert (p := parse(s := "[a]{1}?")) == [[[[[["a"]]]], ""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))  # should change
assert (g := list(gen(p))) == ["a", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))  # should change
assert (p := parse(s := "[ab]{1,2}?")) == [[[[[["a", "b"], ["a", "b", ""]]]], ""]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["aa", "ab", "a", "ba", "bb", "b", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))
# consider testing for group count
# OR
assert (p := parse(s := "|a")) == [[[[""]], [["a"]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["", "a"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a|")) == [[[["a"]], [[""]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", ""], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a|a")) == [[[["a"]], [["a"]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))  # should change
assert (g := list(gen(p))) == ["a", "a"], "".join(map(str, [repr(s), ": generation fail: ", g]))  # should change
assert (p := parse(s := "a|b")) == [[[["a"]], [["b"]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", "b"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "a|b|c")) == [[[["a"]], [["b"]], [["c"]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["a", "b", "c"], "".join(map(str, [repr(s), ": generation fail: ", g]))
# GROUP
assert (p := parse(s := "(a)")) == [[[["a"]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))  # should change
assert (g := list(gen(p))) == ["a"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "(a)a")) == [[[["a"]]], ["a"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))  # should change
assert (g := list(gen(p))) == ["aa"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "(a|b)")) == [[[[[["a"]], [["b"]]]]]], "".join(map(str, [repr(s), ":  parse fail: ", p]))  # should change
assert (g := list(gen(p))) == ["a", "b"], "".join(map(str, [repr(s), ": generation fail: ", g]))
assert (p := parse(s := "(a|b)a")) == [[[[[["a"]], [["b"]]]]], ["a"]], "".join(map(str, [repr(s), ":  parse fail: ", p]))
assert (g := list(gen(p))) == ["aa", "ba"], "".join(map(str, [repr(s), ": generation fail: ", g]))
