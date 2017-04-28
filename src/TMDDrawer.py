import re

testStrList = ["[1sus4]", "[1mMaj7]", "[3m]", "[4m]",
               "[7m7-5]", "[6'7]", "[7,7]", "[7m7]", "[1aug]"]
# @ 300DPI
A4 = [2480.0, 3508.0]
B4 = [2150.0, 3248.0]
A3 = [3508.0, 4960.0]
B3 = [3248.0, 4300.0]


def ChordBuilder(Chord):
    ChordFormRegex = re.compile(
        r"\[(?P<Root>[1-7]('|,)?)(?P<Tonic>(m|aug|dim))?(P<Ext>(Maj|sus|alt))?(?P<TensionNote>(\S*))?\]")
    list(re.finditer(ChordFormRegex, Chord))[0].groupdict()
