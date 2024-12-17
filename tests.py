if __debug__:
    import string

    from gen_pass import gen, parse

    def test(spec, parsed_expected="", generated_expected=None, expect_error=False):
        if expect_error is False:
            parsed = parse(spec)
            assert parsed == parsed_expected, "".join(map(str, [repr(spec), ":  parse fail, got: ", parsed, " expected: ", parsed_expected]))
            generated = list(gen(parsed))
            assert generated == generated_expected, "".join(map(str, [repr(spec), ": generation fail, got: ", generated, " expected: ", generated_expected]))
        else:
            exc = None
            try:
                parse(spec)
            except SyntaxError as e:
                exc = e
            assert exc is not None, expect_error

    # BASE
    test("", [[""]], [""])
    test("a", [["a"]], ["a"])
    test("abc", [["a"], ["b"], ["c"]], ["abc"])
    # IGNORED
    test("^", [[""]], [""])
    test("$", [[""]], [""])
    # ESCAPE
    test("\\", expect_error="unfinished set syntax error")
    test("\\a", [["\a"]], ["\a"])
    test("\\b", [["\b"]], ["\b"])
    test("\\c", [["c"]], ["c"])
    test("\\f", [["\f"]], ["\f"])
    test("\\n", [["\n"]], ["\n"])
    test("\\r", [["\r"]], ["\r"])
    test("\\t", [["\t"]], ["\t"])
    test("\\v", [["\v"]], ["\v"])
    test("\\d", [list(sorted(string.digits))], list(sorted(string.digits)))
    test("\\D", [list(sorted(set(string.printable) - set(string.digits)))], list(sorted(set(string.printable) - set(string.digits))))
    test("\\s", [list(sorted(string.whitespace))], list(sorted(string.whitespace)))
    test("\\S", [list(sorted(set(string.printable) - set(string.whitespace)))], list(sorted(set(string.printable) - set(string.whitespace))))
    test("\\w", [list(sorted(string.ascii_letters + string.digits + "_"))], list(sorted(string.ascii_letters + string.digits + "_")))
    test("\\W", [list(sorted(set(string.printable) - set(string.ascii_letters + string.digits + "_")))], list(sorted(set(string.printable) - set(string.ascii_letters + string.digits + "_"))))
    test("\\x", expect_error="too short hex syntax error")
    test("\\x0", expect_error="too short hex syntax error")
    test("\\x00", [["\x00"]], ["\x00"])
    test("\\x42", [["\x42"]], ["\x42"])
    test("\\xfF", [["\xff"]], ["\xff"])
    test("\\o", expect_error="too short oct syntax error")
    test("\\o0", expect_error="too short oct syntax error")
    test("\\o00", expect_error="too short oct syntax error")
    test("\\o000", [["\000"]], ["\000"])
    test("\\o042", [["\042"]], ["\042"])
    test("\\o377", [["\377"]], ["\377"])
    test("\\o400", expect_error="too big oct syntax error")
    test("\\o777", expect_error="too big oct syntax error")
    test("\\u", expect_error="too short u16 syntax error")
    test("\\u0", expect_error="too short u16 syntax error")
    test("\\u00", expect_error="too short u16 syntax error")
    test("\\u000", expect_error="too short u16 syntax error")
    test("\\u0000", [["\u0000"]], ["\u0000"])
    test("\\u4242", [["\u4242"]], ["\u4242"])
    test("\\ufFfF", [["\uffff"]], ["\uffff"])
    test("\\U", expect_error="too short u32 syntax error")
    test("\\U0", expect_error="too short u32 syntax error")
    test("\\U00", expect_error="too short u32 syntax error")
    test("\\U000", expect_error="too short u32 syntax error")
    test("\\U0000", expect_error="too short u32 syntax error")
    test("\\U00000", expect_error="too short u32 syntax error")
    test("\\U000000", expect_error="too short u32 syntax error")
    test("\\U0000000", expect_error="too short u32 syntax error")
    test("\\U00000000", [["\U00000000"]], ["\U00000000"])
    test("\\U00004242", [[chr(0x00004242)]], [chr(0x00004242)])
    test("\\U0010fFfF", [[chr(0x0010FFFF)]], [chr(0x0010FFFF)])  # why the f this is the biggest supported chr i have no clue, go ask python devs
    test("\\\\a", [["\\"], ["a"]], ["\\a"])
    test("\\a\\b\\c", [["\a"], ["\b"], ["c"]], ["\a\bc"])
    test("\\\\a\\\\b\\\\c", [["\\"], ["a"], ["\\"], ["b"], ["\\"], ["c"]], ["\\a\\b\\c"])
    # SET
    test("[]", [[""]], [""])
    test("[", expect_error="unclosed set syntax error")
    test("[a", expect_error="unclosed set syntax error")
    test("[^", expect_error="unclosed set syntax error")
    test("[^a", expect_error="unclosed set syntax error")
    test("[a]", [["a"]], ["a"])
    test("[^a]", [list(sorted(set(string.printable) - set("a")))], list(sorted(set(string.printable) - set("a"))))
    test("[^ab]", [list(sorted(set(string.printable) - set("ab")))], list(sorted(set(string.printable) - set("ab"))))
    test("[abc]", [["a", "b", "c"]], ["a", "b", "c"])
    test("[a\\bc]", [["a", "\b", "c"]], ["a", "\b", "c"])
    test("[\\\\]", [["\\"]], ["\\"])
    test("[a\\\\c]", [["a", "\\", "c"]], ["a", "\\", "c"])
    test("[[]", [["["]], ["["])
    test("[\\[]", [["["]], ["["])
    test("[a[c]", [["a", "[", "c"]], ["a", "[", "c"])
    test("[a\\[c]", [["a", "[", "c"]], ["a", "[", "c"])
    test("[]]", [["]"]], ["]"])
    test("[\\]]", [["]"]], ["]"])
    test("[a]c]", [["a"], ["c"], ["]"]], ["ac]"])
    test("[a\\]c]", [["a", "]", "c"]], ["a", "]", "c"])
    # COUNT
    test("a{", expect_error="unclosed count syntax error")
    test("a{1", expect_error="unclosed count syntax error")
    test("a{1,", expect_error="unclosed count syntax error")
    test("a{1,1", expect_error="unclosed count syntax error")
    test("a{}", expect_error="count without arguments syntax error")
    test("a{,,}", expect_error="too many count arguments syntax error")
    test("a{a,}", expect_error="bad int in count arguments syntax error")
    test("a{,a}", expect_error="bad int in count arguments syntax error")
    test("a{1,0}", expect_error="bad min max count arguments order syntax error")
    test("a{,}", expect_error="unbound count >=0 syntax error")
    test("a{1,}", expect_error="unbound count >0 syntax error")
    test("a{0}", [[""]], [""])
    test("a{0,0}", [[""]], [""])
    test("a{1}", [[[["a"]]]], ["a"])
    test("a{0,1}", [[[["a", ""]]]], ["a", ""])
    test("a{1,1}", [[[["a"]]]], ["a"])
    test("a{2}", [[[["a"], ["a"]]]], ["aa"])
    test("a{0,2}", [[[["a", ""], ["a", ""]]]], ["aa", "a", "a", ""])  # should change
    test("a{1,2}", [[[["a"], ["a", ""]]]], ["aa", "a"])
    test("a{2,2}", [[[["a"], ["a"]]]], ["aa"])
    test("a{2,3}", [[[["a"], ["a"], ["a", ""]]]], ["aaa", "aa"])
    test("a{2,4}", [[[["a"], ["a"], ["a", ""], ["a", ""]]]], ["aaaa", "aaa", "aaa", "aa"])  # should change
    test("[a]{1}", [[[["a"]]]], ["a"])
    test("[ab]{1,2}", [[[["a", "b"], ["a", "b", ""]]]], ["aa", "ab", "a", "ba", "bb", "b"])
    test("a*", expect_error="unbound count *(>=0) syntax error")
    test("a+", expect_error="unbound count +(>0) syntax error")
    test("a?", [[[["a"]], ""]], ["a", ""])
    test("a?b?", [[[["a"]], ""], [[["b"]], ""]], ["ab", "a", "b", ""])
    test("a??", [[[[[["a"]], ""]], ""]], ["a", "", ""])  # should change
    test("[a]?", [[[["a"]], ""]], ["a", ""])
    test("[abc]?", [[[["a", "b", "c"]], ""]], ["a", "b", "c", ""])
    test("a{0,1}?", [[[[[["a", ""]]]], ""]], ["a", "", ""])  # should change
    test("a{1,1}?", [[[[[["a"]]]], ""]], ["a", ""])    # should change
    test("[a]{1}?", [[[[[["a"]]]], ""]], ["a", ""])  # should change
    test("[ab]{1,2}?", [[[[[["a", "b"], ["a", "b", ""]]]], ""]], ["aa", "ab", "a", "ba", "bb", "b", ""])
    # OR
    test("|", [[[['']], [['']]]], ['', ''])  # should change
    test("|a", [[[[""]], [["a"]]]], ["", "a"])
    test("a|", [[[["a"]], [[""]]]], ["a", ""])
    test("a|a", [[[["a"]], [["a"]]]], ["a", "a"])  # should change
    test("a|b", [[[["a"]], [["b"]]]], ["a", "b"])
    test("a|b|c", [[[["a"]], [["b"]], [["c"]]]], ["a", "b", "c"])
    # GROUP
    # consider testing for group count
    test("(", expect_error="unclosed count syntax error")
    test("(a", expect_error="unclosed count syntax error")
    test("(a)", [[[["a"]]]], ["a"])  # should change
    test("(a)a", [[[["a"]]], ["a"]], ["aa"])  # should change
    test("(a|b)", [[[[[["a"]], [["b"]]]]]], ["a", "b"])  # should change
    test("(a|b)a", [[[[[["a"]], [["b"]]]]], ["a"]], ["aa", "ba"])
