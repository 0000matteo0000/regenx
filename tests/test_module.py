import logging
import string

import pytest

logger = logging.getLogger(__name__)
logging_format = "TEST:%(message)s"
logging.basicConfig(encoding="utf-8", format=logging_format, level=logging.INFO)

if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.append((Path(__file__).parent.parent / "src").absolute().as_posix())

from regenx import calculate_count, gen, parse  # noqa: E402

tests = [
    ("", [[""]], [""], False, None, None, None),
    # BASE
    ("a", [["a"]], ["a"], False, None, None, None),
    ("abc", [["a"], ["b"], ["c"]], ["abc"], False, None, None, None),
    (".", [sorted(set(string.printable))], sorted(set(string.printable)), False, None, None, None),
    # IGNORED
    ("^", [[""]], [""], False, None, None, None),
    ("$", [[""]], [""], False, None, None, None),
    # ESCAPE
    ("\\", None, None, "unfinished set syntax error", None, None, None),
    ("\\.", [["."]], ["."], False, None, None, None),
    ("\\a", [["\a"]], ["\a"], False, None, None, None),
    ("\\b", [["\b"]], ["\b"], False, None, None, None),
    ("\\c", [["c"]], ["c"], False, None, None, None),
    ("\\f", [["\f"]], ["\f"], False, None, None, None),
    ("\\n", [["\n"]], ["\n"], False, None, None, None),
    ("\\r", [["\r"]], ["\r"], False, None, None, None),
    ("\\t", [["\t"]], ["\t"], False, None, None, None),
    ("\\v", [["\v"]], ["\v"], False, None, None, None),
    ("\\d", [sorted(string.digits)], sorted(string.digits), False, None, None, None),
    ("\\D", [sorted(set(string.printable) - set(string.digits))], sorted(set(string.printable) - set(string.digits)), False, None, None, None),
    ("\\s", [sorted(string.whitespace)], sorted(string.whitespace), False, None, None, None),
    ("\\S", [sorted(set(string.printable) - set(string.whitespace))], sorted(set(string.printable) - set(string.whitespace)), False, None, None, None),
    ("\\w", [sorted(string.ascii_letters + string.digits + "_")], sorted(string.ascii_letters + string.digits + "_"), False, None, None, None),
    ("\\W", [sorted(set(string.printable) - set(string.ascii_letters + string.digits + "_"))], sorted(set(string.printable) - set(string.ascii_letters + string.digits + "_")), False, None, None, None),
    ("\\x", None, None, "too short hex syntax error", None, None, None),
    ("\\x0", None, None, "too short hex syntax error", None, None, None),
    ("\\x00", [["\x00"]], ["\x00"], False, None, None, None),
    ("\\x42", [["\x42"]], ["\x42"], False, None, None, None),
    ("\\xfF", [["\xff"]], ["\xff"], False, None, None, None),
    ("\\o", None, None, "too short oct syntax error", None, None, None),
    ("\\o0", None, None, "too short oct syntax error", None, None, None),
    ("\\o00", None, None, "too short oct syntax error", None, None, None),
    ("\\o000", [["\000"]], ["\000"], False, None, None, None),
    ("\\o042", [["\042"]], ["\042"], False, None, None, None),
    ("\\o377", [["\377"]], ["\377"], False, None, None, None),
    ("\\o400", None, None, "too big oct syntax error", None, None, None),
    ("\\o777", None, None, "too big oct syntax error", None, None, None),
    ("\\u", None, None, "too short u16 syntax error", None, None, None),
    ("\\u0", None, None, "too short u16 syntax error", None, None, None),
    ("\\u00", None, None, "too short u16 syntax error", None, None, None),
    ("\\u000", None, None, "too short u16 syntax error", None, None, None),
    ("\\u0000", [["\u0000"]], ["\u0000"], False, None, None, None),
    ("\\u4242", [["\u4242"]], ["\u4242"], False, None, None, None),
    ("\\ufFfF", [["\uffff"]], ["\uffff"], False, None, None, None),
    ("\\U", None, None, "too short u32 syntax error", None, None, None),
    ("\\U0", None, None, "too short u32 syntax error", None, None, None),
    ("\\U00", None, None, "too short u32 syntax error", None, None, None),
    ("\\U000", None, None, "too short u32 syntax error", None, None, None),
    ("\\U0000", None, None, "too short u32 syntax error", None, None, None),
    ("\\U00000", None, None, "too short u32 syntax error", None, None, None),
    ("\\U000000", None, None, "too short u32 syntax error", None, None, None),
    ("\\U0000000", None, None, "too short u32 syntax error", None, None, None),
    ("\\U00000000", [["\U00000000"]], ["\U00000000"], False, None, None, None),
    ("\\U00004242", [[chr(0x00004242)]], [chr(0x00004242)], False, None, None, None),
    ("\\U0010fFfF", [[chr(0x0010FFFF)]], [chr(0x0010FFFF)], False, None, None, None),  # why the f this is the biggest supported chr i have no clue, go ask python devs, False, None, None, None),
    ("\\\\a", [["\\"], ["a"]], ["\\a"], False, None, None, None),
    ("\\a\\b\\c", [["\a"], ["\b"], ["c"]], ["\a\bc"], False, None, None, None),
    ("\\\\a\\\\b\\\\c", [["\\"], ["a"], ["\\"], ["b"], ["\\"], ["c"]], ["\\a\\b\\c"], False, None, None, None),
    # SET
    ("[]", [[""]], [""], False, None, None, None),
    ("[", None, None, "unclosed set syntax error", None, None, None),
    ("[a", None, None, "unclosed set syntax error", None, None, None),
    ("[^", None, None, "unclosed set syntax error", None, None, None),
    ("[^a", None, None, "unclosed set syntax error", None, None, None),
    ("[a]", [["a"]], ["a"], False, None, None, None),
    ("[^a]", [sorted(set(string.printable) - set("a"))], sorted(set(string.printable) - set("a")), False, None, None, None),
    ("[^ab]", [sorted(set(string.printable) - set("ab"))], sorted(set(string.printable) - set("ab")), False, None, None, None),
    ("[abc]", [["a", "b", "c"]], ["a", "b", "c"], False, None, None, None),
    ("[a\\bc]", [["a", "\b", "c"]], ["a", "\b", "c"], False, None, None, None),
    ("[\\\\]", [["\\"]], ["\\"], False, None, None, None),
    ("[a\\\\c]", [["a", "\\", "c"]], ["a", "\\", "c"], False, None, None, None),
    ("[[]", [["["]], ["["], False, None, None, None),
    ("[\\[]", [["["]], ["["], False, None, None, None),
    ("[a[c]", [["a", "[", "c"]], ["a", "[", "c"], False, None, None, None),
    ("[a\\[c]", [["a", "[", "c"]], ["a", "[", "c"], False, None, None, None),
    ("[]]", [["]"]], ["]"], False, None, None, None),
    ("[\\]]", [["]"]], ["]"], False, None, None, None),
    ("[a]c]", [["a"], ["c"], ["]"]], ["ac]"], False, None, None, None),
    ("[a\\]c]", [["a", "]", "c"]], ["a", "]", "c"], False, None, None, None),
    # COUNT
    ("a{", None, None, "unclosed count syntax error", None, None, None),
    ("a{1", None, None, "unclosed count syntax error", None, None, None),
    ("a{1,", None, None, "unclosed count syntax error", None, None, None),
    ("a{1,1", None, None, "unclosed count syntax error", None, None, None),
    ("a{}", None, None, "count without arguments syntax error", None, None, None),
    ("a{,,}", None, None, "too many count arguments syntax error", None, None, None),
    ("a{a,}", None, None, "bad int in count arguments syntax error", None, None, None),
    ("a{,a}", None, None, "bad int in count arguments syntax error", None, None, None),
    ("a{1,0}", None, None, "bad min max count arguments order syntax error", None, None, None),
    ("a{,}", None, None, "unbound count >=0 syntax error", None, None, None),
    ("a{1,}", None, None, "unbound count >0 syntax error", None, None, None),
    ("a{0}", [[""]], [""], False, None, None, None),
    ("a{0,0}", [[""]], [""], False, None, None, None),
    ("a{1}", [[[["a"]]]], ["a"], False, None, None, None),
    ("a{0,1}", [[[["a", ""]]]], ["a", ""], False, None, None, None),
    ("a{1,1}", [[[["a"]]]], ["a"], False, None, None, None),
    ("a{2}", [[[["a"], ["a"]]]], ["aa"], False, None, None, None),
    ("a{0,2}", [[[["a", ""], ["a", ""]]]], ["aa", "a", "a", ""], False, None, None, None),  # should change
    ("a{1,2}", [[[["a"], ["a", ""]]]], ["aa", "a"], False, None, None, None),
    ("a{2,2}", [[[["a"], ["a"]]]], ["aa"], False, None, None, None),
    ("a{2,3}", [[[["a"], ["a"], ["a", ""]]]], ["aaa", "aa"], False, None, None, None),
    ("a{2,4}", [[[["a"], ["a"], ["a", ""], ["a", ""]]]], ["aaaa", "aaa", "aaa", "aa"], False, None, None, None),  # should change
    ("[a]{1}", [[[["a"]]]], ["a"], False, None, None, None),
    ("[ab]{1,2}", [[[["a", "b"], ["a", "b", ""]]]], ["aa", "ab", "a", "ba", "bb", "b"], False, None, None, None),
    ("a*", None, None, "unbound count *(>=0) syntax error", None, None, None),
    ("a+", None, None, "unbound count +(>0) syntax error", None, None, None),
    # OR
    ("|", [[[[""]], [[""]]]], ["", ""], False, None, None, None),  # should change
    ("|a", [[[[""]], [["a"]]]], ["", "a"], False, None, None, None),
    ("a|", [[[["a"]], [[""]]]], ["a", ""], False, None, None, None),
    ("a|a", [[[["a"]], [["a"]]]], ["a", "a"], False, None, None, None),  # should change
    ("a|b", [[[["a"]], [["b"]]]], ["a", "b"], False, None, None, None),
    ("a|b|c", [[[["a"]], [["b"]], [["c"]]]], ["a", "b", "c"], False, None, None, None),
    ("a|", [[[["a"]], [[""]]]], ["a", ""], False, None, None, None),
    ("[a]|", [[[["a"]], [[""]]]], ["a", ""], False, None, None, None),
    ("[abc]|", [[[["a", "b", "c"]], [[""]]]], ["a", "b", "c", ""], False, None, None, None),
    ("a{0,1}|", [[[[[["a", ""]]]], [[""]]]], ["a", "", ""], False, None, None, None),  # should change
    ("a{1,1}|", [[[[[["a"]]]], [[""]]]], ["a", ""], False, None, None, None),  # should change
    ("[a]{1}|", [[[[[["a"]]]], [[""]]]], ["a", ""], False, None, None, None),  # should change
    ("[ab]{1,2}|", [[[[[["a", "b"], ["a", "b", ""]]]], [[""]]]], ["aa", "ab", "a", "ba", "bb", "b", ""], False, None, None, None),
    ("[c-a]", [["c", "b", "a"]], ["c", "b", "a"], False, None, None, None),
    ("[a-c]", [["a", "b", "c"]], ["a", "b", "c"], False, None, None, None),
    ("[0-9]", [list(string.digits)], list(string.digits), False, None, None, None),
    ("[a-z]", [list(string.ascii_lowercase)], list(string.ascii_lowercase), False, None, None, None),
    ("[A-Z]", [list(string.ascii_uppercase)], list(string.ascii_uppercase), False, None, None, None),
    ("[a-zA-Z]", [list(string.ascii_letters)], list(string.ascii_letters), False, None, None, None),
    ("[0-9a-zA-Z]", [list(string.digits + string.ascii_letters)], list(string.digits + string.ascii_letters), False, None, None, None),
    # GROUP
    # consider testing for group count
    ("(", None, None, "unclosed count syntax error", None, None, None),
    ("(a", None, None, "unclosed count syntax error", None, None, None),
    ("(a)", [[[["a"]]]], ["a"], False, None, None, None),  # should change
    ("(a)a", [[[["a"]]], ["a"]], ["aa"], False, None, None, None),  # should change
    ("(a|b)", [[[[[["a"]], [["b"]]]]]], ["a", "b"], False, None, None, None),  # should change
    ("(a|b)a", [[[[[["a"]], [["b"]]]]], ["a"]], ["aa", "ba"], False, None, None, None),
    ("(a|)(b|)", [[[[[["a"]], [[""]]]]], [[[[["b"]], [[""]]]]]], ["ab", "a", "b", ""], False, None, None, None),
    ("(a|)|", [[[[[[[["a"]], [[""]]]]]], [[""]]]], ["a", "", ""], False, None, None, None),  # should change
    # # # EXTRA
    # ("([a-z0-9_\.\-]{1})@([\da-z\.\-]{1})\.([a-z\.]{2})", None, ['a@0.aa', 'a@0.ab', 'a@0.ac', 'a@0.ad', 'a@0.ae'], False, 5),
    # ("employ(|er|ee|ment|ing|able)", None, ["employ", "employer", "employee", "employment", "employing", "employable"], False, None, None, None),
    # ("[a-f0-9]{2}", None, ['aa', 'ab', 'ac', 'ad', 'ae'], False, 5),
    # ("[A-Fa-f0-9]{2}", None, ['AA', 'AB', 'AC', 'AD', 'AE'], False, 5),
    # ("<tag>[^<]{1}</tag>", None, ['<tag>\t</tag>', '<tag>\n</tag>', '<tag>\x0b</tag>', '<tag>\x0c</tag>', '<tag>\r</tag>'], False, 5),
    # ("<[\s]{1}tag[^>]{1}>[^<]{1}<[\s]{1}/[\s]{1}tag[\s]{1}>", None, ['<\ttag\t>\t<\t/\ttag\t>', '<\ttag\t>\t<\t/\ttag\n>', '<\ttag\t>\t<\t/\ttag\x0b>', '<\ttag\t>\t<\t/\ttag\x0c>', '<\ttag\t>\t<\t/\ttag\r>'], False, 5),
    # ("(https?:\/\/)?([\da-z.\-]{1,2})\.([a-z.]{2,6})([\/\w \.\-]{1}){2}\/?", None, ['https?://?00.aaaaaa///?', 'https?://?00.aaaaaa/0/?', 'https?://?00.aaaaaa/1/?', 'https?://?00.aaaaaa/2/?', 'https?://?00.aaaaaa/3/?'], False, 5),
    # ("[]", None, [''], False, None, None, None),
    # ("[^]", None, list(sorted(string.printable)), False, None, None, None),
    # ("[.]", None, ['.'], False, None, None, None),
    # ("[^.]", None, None, False, None, None, None),
    # ("[b-a]", None, None, False, None, None, None),
    # ("[a-\w]", None, None, False, None, None, None),
    # ("[a-\d]", None, None, False, None, None, None),
    # ("[^\Wf]", None, None, False, None, None, None),
    # ("[^^]", None, None, False, None, None, None),
    # ("[四十二]", None, None, False, None, None, None),
    # ("\d\D\s\S\w\W", None, None, False, None, None, None),
    # ("[\dabc][\D123][\sabc][\S\t][\w\x00][\Wabc]", None, None, False, None, None, None),
    # ("()", None, None, False, None, None, None),
    # ("(|)", None, None, False, None, None, None),
    # ("(||)", None, None, False, None, None, None),
    # ("(|||)", None, None, False, None, None, None),
    # ("(a|)", None, None, False, None, None, None),
    # ("(|b)", None, None, False, None, None, None),
    # ("(a|b)", None, None, False, None, None, None),
    # ("|", None, None, False, None, None, None),
    # ("a*", None, None, False, None, None, None),
    # ("a+", None, None, False, None, None, None),
    # ("a?", None, None, False, None, None, None),
    # ("a*?", None, None, False, None, None, None),
    # ("a+?", None, None, False, None, None, None),
    # ("a??", None, None, False, None, None, None),
    # ("a{2}", None, None, False, None, None, None),
    # ("a{2}?", None, None, False, None, None, None),
    # ("a{,2}", None, None, False, None, None, None),
    # ("a{,2}?", None, None, False, None, None, None),
    # ("a{2,}", None, None, False, None, None, None),
    # ("a{2,}?", None, None, False, None, None, None),
    # ("a{2,3}", None, None, False, None, None, None),
    # ("a{2,3}?", None, None, False, None, None, None),
    # ("abc+|def+", None, None, False, None, None, None),
    # ("ab+c|de+f", None, None, False, None, None, None),
    # ("a*{4}", None, None, False, None, None, None),
    # ("(a*){4}", None, None, False, None, None, None),
    # ("(){0,1}", None, None, False, None, None, None),
    # ("(){1,2}", None, None, False, None, None, None),
    # ("()+", None, None, False, None, None, None),
    # ("(a*?)*", None, None, False, None, None, None),
    # ("(a*)*", None, None, False, None, None, None),
    # ("+", None, None, False, None, None, None),
    # ("(a+a+)+b", None, None, False, None, None, None),
    # ("(a+?a+?)+?b", None, None, False, None, None, None),
    # ("[bc]*(cd)+", None, None, False, None, None, None),
    # ("\$\.\(\)\*\+\?\[\\]\^\{\|\}", None, None, False, None, None, None),
    # ("\0\t\n\r\v\f\\", None, None, False, None, None, None),
    # ("\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B\x2C\x2D\x2E\x2F", None, None, False, None, None, None),
    # ("\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4A\x4B\x4C\x4D\x4E\x4F\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5A\x5B\x5C\x5D\x5E\x5F", None, None, False, None, None, None),
    # ("\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6A\x6B\x6C\x6D\x6E\x6F\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7A\x7B\x7C\x7D\x7E\x7F\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8A\x8B\x8C\x8D\x8E\x8F", None, None, False, None, None, None),
    # ("\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9A\x9B\x9C\x9D\x9E\x9F\xA0\xA1\xA2\xA3\xA4\xA5\xA6\xA7\xA8\xA9\xAA\xAB\xAC\xAD\xAE\xAF\xB0\xB1\xB2\xB3\xB4\xB5\xB6\xB7\xB8\xB9\xBA\xBB\xBC\xBD\xBE\xBF", None, None, False, None, None, None),
    # ("\xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xCB\xCC\xCD\xCE\xCF\xD0\xD1\xD2\xD3\xD4\xD5\xD6\xD7\xD8\xD9\xDA\xDB\xDC\xDD\xDE\xDF\xE0\xE1\xE2\xE3\xE4\xE5\xE6\xE7\xE8\xE9\xEA\xEB\xEC\xED\xEE\xEF", None, None, False, None, None, None),
    # ("2", None, None, False, None, None, None),
    # ("\xF0\xF1\xF2\xF3\xF4\xF5\xF6\xF7\xF8\xF9\xFA\xFB\xFC\xFD\xFE\xFF", None, None, False, None, None, None),
    # ("四十二", None, None, False, None, None, None),
]


@pytest.mark.parametrize(
    ("spec", "parsed_expected", "generated_expected", "expect_error", "count_expected", "skip", "limit"),
    tests,
)
def test(spec, parsed_expected, generated_expected, expect_error, count_expected, skip, limit):
    logger.info("-" * 100)
    logger.info("testing: %r %r %r %r %r %r", spec, parsed_expected, generated_expected, expect_error, count_expected, limit)
    if expect_error is False:
        parsed = parse(spec)
        if parsed_expected is not None:
            assert parsed == parsed_expected, "".join(map(str, [repr(spec), ":  parse fail, got: ", parsed, " expected: ", parsed_expected]))
        if count_expected is None:
            # assert skip is None and limit is None, "if you provide a limited output check you must provide a count check"
            count_expected = len(generated_expected)
        if limit is None:
            if skip is None:  # noqa: SIM108
                output_count_expected = count_expected
            else:
                output_count_expected = count_expected - min(skip, count_expected)
                # generated_expected = generated_expected[skip:]
        else:
            output_count_expected = min(limit, count_expected)
            # generated_expected = generated_expected[skip:skip+limit]
        count = calculate_count(parsed)
        assert count == count_expected, "".join(map(str, [repr(spec), ": count fail, got: ", count, " expected: ", count_expected]))
        if skip is None:
            skip = 0
        generated = list(gen(parsed, skip=skip, limit=limit))
        assert len(generated) == output_count_expected, "".join(map(str, [repr(spec), ": output count fail, got: ", len(generated), " expected: ", output_count_expected]))
        assert generated == generated_expected, "".join(map(str, [repr(spec), ": generation fail, got: ", generated, " expected: ", generated_expected]))
    else:
        exc = None
        try:
            parse(spec)
        except SyntaxError as e:
            exc = e
        assert exc is not None, expect_error
    logger.info("-" * 100)


if __name__ == "__main__":
    for t in tests:
        test(*t)
