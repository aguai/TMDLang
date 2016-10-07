import cairo
A4=(2480, 3508) # @ 300DPI
def ChordDrawer(Root, Bass, Quality, Position) : 
    # Root:     char : with or without sup Flat or Sharp
    # Bass:     char : under a slash '/' ('' for no Alternative bass note to draw)
    # Quality:  str  : Interval included ex: symbol like +, Δ(Maj7), o(dim), alt, sus, etc. 
    # Position: tuple: (x,y): position to draw this Chord 