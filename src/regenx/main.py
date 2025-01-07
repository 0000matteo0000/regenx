# SPDX-FileCopyrightText: 2024-present 0000matteo0000 <matteo.sid@hotmail.it>
#
# SPDX-License-Identifier: MIT

import sys

from regenx import gen, parse

if __name__ == "__main__":
    for i, rule in enumerate(sys.argv):
        if i == 0:
            continue
        print(i, rule, file=sys.stderr)  # noqa: T201
        for g in gen(parse(rule)):
            print(g)  # noqa: T201
