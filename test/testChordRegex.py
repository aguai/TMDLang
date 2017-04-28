import re

regex = r"\[(?P<Root>[1-7]('|,)?)(?P<Tonic>(m|aug|dim))?(P<Ext>(Maj|sus|alt))?(?P<TensionNote>(\S*))?\]"

test_str = ("[1sus4]\n"
            "[1mMaj7]\n"
            "[3m]\n"
            "[4m]\n"
            "[7m7-5]\n"
            "[6,7]\n"
            "[7,7]\n"
            "[7m7]\n"
            "[1aug]")

matches = re.finditer(regex, test_str)

for matchNum, match in enumerate(matches):
    matchNum = matchNum + 1

    print("Match {matchNum} was found at {start}-{end}: {match}".format(
        matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()))

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1

        print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                        start=match.start(groupNum), end=match.end(groupNum), group=match.group(groupNum)))
