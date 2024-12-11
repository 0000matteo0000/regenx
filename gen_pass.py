import sys

from gen import gen, parse

if __debug__:
    import tests

if __name__ == "__main__":
    for i, rule in enumerate(sys.argv):
        if i == 0:
            continue
        print(i, rule, file=sys.stderr)
        for g in gen(parse(rule)):
            print(g)
