import string

import pytest

if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.append((Path(__file__).parent.parent / "src").absolute().as_posix())

from regenx import gen, parse

tests = [
    ("", [[""]], [""], False, None),
    # BASE
    ("a", [["a"]], ["a"], False, None),
    ("abc", [["a"], ["b"], ["c"]], ["abc"], False, None),
    (".", [sorted(set(string.printable))], sorted(set(string.printable)), False, None),
    # IGNORED
    ("^", [[""]], [""], False, None),
    ("$", [[""]], [""], False, None),
    # ESCAPE
    ("\\", None, None, "unfinished set syntax error", None),
    ("\\.", [["."]], ["."], False, None),
    ("\\a", [["\a"]], ["\a"], False, None),
    ("\\b", [["\b"]], ["\b"], False, None),
    ("\\c", [["c"]], ["c"], False, None),
    ("\\f", [["\f"]], ["\f"], False, None),
    ("\\n", [["\n"]], ["\n"], False, None),
    ("\\r", [["\r"]], ["\r"], False, None),
    ("\\t", [["\t"]], ["\t"], False, None),
    ("\\v", [["\v"]], ["\v"], False, None),
    ("\\d", [sorted(string.digits)], sorted(string.digits), False, None),
    ("\\D", [sorted(set(string.printable) - set(string.digits))], sorted(set(string.printable) - set(string.digits)), False, None),
    ("\\s", [sorted(string.whitespace)], sorted(string.whitespace), False, None),
    ("\\S", [sorted(set(string.printable) - set(string.whitespace))], sorted(set(string.printable) - set(string.whitespace)), False, None),
    ("\\w", [sorted(string.ascii_letters + string.digits + "_")], sorted(string.ascii_letters + string.digits + "_"), False, None),
    ("\\W", [sorted(set(string.printable) - set(string.ascii_letters + string.digits + "_"))], sorted(set(string.printable) - set(string.ascii_letters + string.digits + "_")), False, None),
    ("\\x", None, None, "too short hex syntax error", None),
    ("\\x0", None, None, "too short hex syntax error", None),
    ("\\x00", [["\x00"]], ["\x00"], False, None),
    ("\\x42", [["\x42"]], ["\x42"], False, None),
    ("\\xfF", [["\xff"]], ["\xff"], False, None),
    ("\\o", None, None, "too short oct syntax error", None),
    ("\\o0", None, None, "too short oct syntax error", None),
    ("\\o00", None, None, "too short oct syntax error", None),
    ("\\o000", [["\000"]], ["\000"], False, None),
    ("\\o042", [["\042"]], ["\042"], False, None),
    ("\\o377", [["\377"]], ["\377"], False, None),
    ("\\o400", None, None, "too big oct syntax error", None),
    ("\\o777", None, None, "too big oct syntax error", None),
    ("\\u", None, None, "too short u16 syntax error", None),
    ("\\u0", None, None, "too short u16 syntax error", None),
    ("\\u00", None, None, "too short u16 syntax error", None),
    ("\\u000", None, None, "too short u16 syntax error", None),
    ("\\u0000", [["\u0000"]], ["\u0000"], False, None),
    ("\\u4242", [["\u4242"]], ["\u4242"], False, None),
    ("\\ufFfF", [["\uffff"]], ["\uffff"], False, None),
    ("\\U", None, None, "too short u32 syntax error", None),
    ("\\U0", None, None, "too short u32 syntax error", None),
    ("\\U00", None, None, "too short u32 syntax error", None),
    ("\\U000", None, None, "too short u32 syntax error", None),
    ("\\U0000", None, None, "too short u32 syntax error", None),
    ("\\U00000", None, None, "too short u32 syntax error", None),
    ("\\U000000", None, None, "too short u32 syntax error", None),
    ("\\U0000000", None, None, "too short u32 syntax error", None),
    ("\\U00000000", [["\U00000000"]], ["\U00000000"], False, None),
    ("\\U00004242", [[chr(0x00004242)]], [chr(0x00004242)], False, None),
    ("\\U0010fFfF", [[chr(0x0010FFFF)]], [chr(0x0010FFFF)], False, None),  # why the f this is the biggest supported chr i have no clue, go ask python devs, False, None),
    ("\\\\a", [["\\"], ["a"]], ["\\a"], False, None),
    ("\\a\\b\\c", [["\a"], ["\b"], ["c"]], ["\a\bc"], False, None),
    ("\\\\a\\\\b\\\\c", [["\\"], ["a"], ["\\"], ["b"], ["\\"], ["c"]], ["\\a\\b\\c"], False, None),
    # SET
    ("[]", [[""]], [""], False, None),
    ("[", None, None, "unclosed set syntax error", None),
    ("[a", None, None, "unclosed set syntax error", None),
    ("[^", None, None, "unclosed set syntax error", None),
    ("[^a", None, None, "unclosed set syntax error", None),
    ("[a]", [["a"]], ["a"], False, None),
    ("[^a]", [sorted(set(string.printable) - set("a"))], sorted(set(string.printable) - set("a")), False, None),
    ("[^ab]", [sorted(set(string.printable) - set("ab"))], sorted(set(string.printable) - set("ab")), False, None),
    ("[abc]", [["a", "b", "c"]], ["a", "b", "c"], False, None),
    ("[a\\bc]", [["a", "\b", "c"]], ["a", "\b", "c"], False, None),
    ("[\\\\]", [["\\"]], ["\\"], False, None),
    ("[a\\\\c]", [["a", "\\", "c"]], ["a", "\\", "c"], False, None),
    ("[[]", [["["]], ["["], False, None),
    ("[\\[]", [["["]], ["["], False, None),
    ("[a[c]", [["a", "[", "c"]], ["a", "[", "c"], False, None),
    ("[a\\[c]", [["a", "[", "c"]], ["a", "[", "c"], False, None),
    ("[]]", [["]"]], ["]"], False, None),
    ("[\\]]", [["]"]], ["]"], False, None),
    ("[a]c]", [["a"], ["c"], ["]"]], ["ac]"], False, None),
    ("[a\\]c]", [["a", "]", "c"]], ["a", "]", "c"], False, None),
    # COUNT
    ("a{", None, None, "unclosed count syntax error", None),
    ("a{1", None, None, "unclosed count syntax error", None),
    ("a{1,", None, None, "unclosed count syntax error", None),
    ("a{1,1", None, None, "unclosed count syntax error", None),
    ("a{}", None, None, "count without arguments syntax error", None),
    ("a{,,}", None, None, "too many count arguments syntax error", None),
    ("a{a,}", None, None, "bad int in count arguments syntax error", None),
    ("a{,a}", None, None, "bad int in count arguments syntax error", None),
    ("a{1,0}", None, None, "bad min max count arguments order syntax error", None),
    ("a{,}", None, None, "unbound count >=0 syntax error", None),
    ("a{1,}", None, None, "unbound count >0 syntax error", None),
    ("a{0}", [[""]], [""], False, None),
    ("a{0,0}", [[""]], [""], False, None),
    ("a{1}", [[[["a"]]]], ["a"], False, None),
    ("a{0,1}", [[[["a", ""]]]], ["a", ""], False, None),
    ("a{1,1}", [[[["a"]]]], ["a"], False, None),
    ("a{2}", [[[["a"], ["a"]]]], ["aa"], False, None),
    ("a{0,2}", [[[["a", ""], ["a", ""]]]], ["aa", "a", "a", ""], False, None),  # should change
    ("a{1,2}", [[[["a"], ["a", ""]]]], ["aa", "a"], False, None),
    ("a{2,2}", [[[["a"], ["a"]]]], ["aa"], False, None),
    ("a{2,3}", [[[["a"], ["a"], ["a", ""]]]], ["aaa", "aa"], False, None),
    ("a{2,4}", [[[["a"], ["a"], ["a", ""], ["a", ""]]]], ["aaaa", "aaa", "aaa", "aa"], False, None),  # should change
    ("[a]{1}", [[[["a"]]]], ["a"], False, None),
    ("[ab]{1,2}", [[[["a", "b"], ["a", "b", ""]]]], ["aa", "ab", "a", "ba", "bb", "b"], False, None),
    ("a*", None, None, "unbound count *(>=0) syntax error", None),
    ("a+", None, None, "unbound count +(>0) syntax error", None),
    # OR
    ("|", [[[[""]], [[""]]]], ["", ""], False, None),  # should change
    ("|a", [[[[""]], [["a"]]]], ["", "a"], False, None),
    ("a|", [[[["a"]], [[""]]]], ["a", ""], False, None),
    ("a|a", [[[["a"]], [["a"]]]], ["a", "a"], False, None),  # should change
    ("a|b", [[[["a"]], [["b"]]]], ["a", "b"], False, None),
    ("a|b|c", [[[["a"]], [["b"]], [["c"]]]], ["a", "b", "c"], False, None),
    ("a|", [[[["a"]], [[""]]]], ["a", ""], False, None),
    ("[a]|", [[[["a"]], [[""]]]], ["a", ""], False, None),
    ("[abc]|", [[[["a", "b", "c"]], [[""]]]], ["a", "b", "c", ""], False, None),
    ("a{0,1}|", [[[[[["a", ""]]]], [[""]]]], ["a", "", ""], False, None),  # should change
    ("a{1,1}|", [[[[[["a"]]]], [[""]]]], ["a", ""], False, None),  # should change
    ("[a]{1}|", [[[[[["a"]]]], [[""]]]], ["a", ""], False, None),  # should change
    ("[ab]{1,2}|", [[[[[["a", "b"], ["a", "b", ""]]]], [[""]]]], ["aa", "ab", "a", "ba", "bb", "b", ""], False, None),
    ("[c-a]", [["c", "b", "a"]], ["c", "b", "a"], False, None),
    ("[a-c]", [["a", "b", "c"]], ["a", "b", "c"], False, None),
    ("[0-9]", [list(string.digits)], list(string.digits), False, None),
    ("[a-z]", [list(string.ascii_lowercase)], list(string.ascii_lowercase), False, None),
    ("[A-Z]", [list(string.ascii_uppercase)], list(string.ascii_uppercase), False, None),
    ("[a-zA-Z]", [list(string.ascii_letters)], list(string.ascii_letters), False, None),
    ("[0-9a-zA-Z]", [list(string.digits + string.ascii_letters)], list(string.digits + string.ascii_letters), False, None),
    # GROUP
    # consider testing for group count
    ("(", None, None, "unclosed count syntax error", None),
    ("(a", None, None, "unclosed count syntax error", None),
    ("(a)", [[[["a"]]]], ["a"], False, None),  # should change
    ("(a)a", [[[["a"]]], ["a"]], ["aa"], False, None),  # should change
    ("(a|b)", [[[[[["a"]], [["b"]]]]]], ["a", "b"], False, None),  # should change
    ("(a|b)a", [[[[[["a"]], [["b"]]]]], ["a"]], ["aa", "ba"], False, None),
    ("(a|)(b|)", [[[[[["a"]], [[""]]]]], [[[[["b"]], [[""]]]]]], ["ab", "a", "b", ""], False, None),
    ("(a|)|", [[[[[[[["a"]], [[""]]]]]], [[""]]]], ["a", "", ""], False, None),  # should change
    # # # EXTRA
    # ("([a-z0-9_\.\-]{1})@([\da-z\.\-]{1})\.([a-z\.]{2})", None, ['a@0.aa', 'a@0.ab', 'a@0.ac', 'a@0.ad', 'a@0.ae'], False, 5),
    # ("employ(|er|ee|ment|ing|able)", None, ["employ", "employer", "employee", "employment", "employing", "employable"], False, None),
    # ("[a-f0-9]{2}", None, ['aa', 'ab', 'ac', 'ad', 'ae'], False, 5),
    # ("[A-Fa-f0-9]{2}", None, ['AA', 'AB', 'AC', 'AD', 'AE'], False, 5),
    # ("<tag>[^<]{1}</tag>", None, ['<tag>\t</tag>', '<tag>\n</tag>', '<tag>\x0b</tag>', '<tag>\x0c</tag>', '<tag>\r</tag>'], False, 5),
    # ("<[\s]{1}tag[^>]{1}>[^<]{1}<[\s]{1}/[\s]{1}tag[\s]{1}>", None, ['<\ttag\t>\t<\t/\ttag\t>', '<\ttag\t>\t<\t/\ttag\n>', '<\ttag\t>\t<\t/\ttag\x0b>', '<\ttag\t>\t<\t/\ttag\x0c>', '<\ttag\t>\t<\t/\ttag\r>'], False, 5),
    # ("(https?:\/\/)?([\da-z.\-]{1,2})\.([a-z.]{2,6})([\/\w \.\-]{1}){2}\/?", None, ['https?://?00.aaaaaa///?', 'https?://?00.aaaaaa/0/?', 'https?://?00.aaaaaa/1/?', 'https?://?00.aaaaaa/2/?', 'https?://?00.aaaaaa/3/?'], False, 5),
    # ("[]", None, [''], False, None),
    # ("[^]", None, list(sorted(string.printable)), False, None),
    # ("[.]", None, ['.'], False, None),
    # ("[^.]", None, None, False, None),
    # ("[b-a]", None, None, False, None),
    # ("[a-\w]", None, None, False, None),
    # ("[a-\d]", None, None, False, None),
    # ("[^\Wf]", None, None, False, None),
    # ("[^^]", None, None, False, None),
    # ("[四十二]", None, None, False, None),
    # ("\d\D\s\S\w\W", None, None, False, None),
    # ("[\dabc][\D123][\sabc][\S\t][\w\x00][\Wabc]", None, None, False, None),
    # ("()", None, None, False, None),
    # ("(|)", None, None, False, None),
    # ("(||)", None, None, False, None),
    # ("(|||)", None, None, False, None),
    # ("(a|)", None, None, False, None),
    # ("(|b)", None, None, False, None),
    # ("(a|b)", None, None, False, None),
    # ("|", None, None, False, None),
    # ("a*", None, None, False, None),
    # ("a+", None, None, False, None),
    # ("a?", None, None, False, None),
    # ("a*?", None, None, False, None),
    # ("a+?", None, None, False, None),
    # ("a??", None, None, False, None),
    # ("a{2}", None, None, False, None),
    # ("a{2}?", None, None, False, None),
    # ("a{,2}", None, None, False, None),
    # ("a{,2}?", None, None, False, None),
    # ("a{2,}", None, None, False, None),
    # ("a{2,}?", None, None, False, None),
    # ("a{2,3}", None, None, False, None),
    # ("a{2,3}?", None, None, False, None),
    # ("abc+|def+", None, None, False, None),
    # ("ab+c|de+f", None, None, False, None),
    # ("a*{4}", None, None, False, None),
    # ("(a*){4}", None, None, False, None),
    # ("(){0,1}", None, None, False, None),
    # ("(){1,2}", None, None, False, None),
    # ("()+", None, None, False, None),
    # ("(a*?)*", None, None, False, None),
    # ("(a*)*", None, None, False, None),
    # ("+", None, None, False, None),
    # ("(a+a+)+b", None, None, False, None),
    # ("(a+?a+?)+?b", None, None, False, None),
    # ("[bc]*(cd)+", None, None, False, None),
    # ("\$\.\(\)\*\+\?\[\\]\^\{\|\}", None, None, False, None),
    # ("\0\t\n\r\v\f\\", None, None, False, None),
    # ("\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B\x2C\x2D\x2E\x2F", None, None, False, None),
    # ("\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4A\x4B\x4C\x4D\x4E\x4F\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5A\x5B\x5C\x5D\x5E\x5F", None, None, False, None),
    # ("\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6A\x6B\x6C\x6D\x6E\x6F\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7A\x7B\x7C\x7D\x7E\x7F\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8A\x8B\x8C\x8D\x8E\x8F", None, None, False, None),
    # ("\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9A\x9B\x9C\x9D\x9E\x9F\xA0\xA1\xA2\xA3\xA4\xA5\xA6\xA7\xA8\xA9\xAA\xAB\xAC\xAD\xAE\xAF\xB0\xB1\xB2\xB3\xB4\xB5\xB6\xB7\xB8\xB9\xBA\xBB\xBC\xBD\xBE\xBF", None, None, False, None),
    # ("\xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xCB\xCC\xCD\xCE\xCF\xD0\xD1\xD2\xD3\xD4\xD5\xD6\xD7\xD8\xD9\xDA\xDB\xDC\xDD\xDE\xDF\xE0\xE1\xE2\xE3\xE4\xE5\xE6\xE7\xE8\xE9\xEA\xEB\xEC\xED\xEE\xEF", None, None, False, None),
    # ("2", None, None, False, None),
    # ("\xF0\xF1\xF2\xF3\xF4\xF5\xF6\xF7\xF8\xF9\xFA\xFB\xFC\xFD\xFE\xFF", None, None, False, None),
    # ("四十二", None, None, False, None),
]


@pytest.mark.parametrize(
    ("spec", "parsed_expected", "generated_expected", "expect_error", "count"),
    tests,
)
def test(spec, parsed_expected, generated_expected, expect_error, count):
    print("-" * 100)  # noqa: T201
    print("testing:", repr(spec), repr(parsed_expected), repr(generated_expected), repr(expect_error), repr(count))  # noqa: T201
    if expect_error is False:
        parsed = parse(spec)
        if parsed_expected is not None:
            assert parsed == parsed_expected, "".join(map(str, [repr(spec), ":  parse fail, got: ", parsed, " expected: ", parsed_expected]))
        generated = list(gen(parsed, count=count))
        assert generated == generated_expected, "".join(map(str, [repr(spec), ": generation fail, got: ", generated, " expected: ", generated_expected]))
    else:
        exc = None
        try:
            parse(spec)
        except SyntaxError as e:
            exc = e
        assert exc is not None, expect_error
    print("-" * 100)  # noqa: T201


if __name__ == "__main__":
    for t in tests:
        test(*t)
