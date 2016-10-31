# -*- coding: utf8 -*-
import cairo
# @ 300DPI
A4=[2480.0, 3508.0]
B4=[3248.0, 2150.0]
A3=[4960.0, 3508.0]
B3=[3248.0, 4300.0]


def ChordDrawer(Surface ,ChordList) :
    # NAME: Song Name (with page#?)
    # TYPE: {PDF, SVG}
    # Size: {A3, A4, B4, B3}
    # ChordList: [Chord，...]
    # Chord :[Root-> {'chr'/[1-7]/,['#'|'b'|''] }, Bass -> 'chr', Quality -> 'str', Position -> {x, y}]
    # Surface:  cairo.Surface
    # Root:     char : with or without sup Flat or Sharp
    # Bass:     char : under a slash '/' ('' for no Alternative bass note to draw)
    # Quality:  str  : Interval included ex: symbol like +, Δ(Maj7), o(dim), alt, sus, etc.
    # Position: tuple: (x,y): position to draw this Chord
    #generate size here
    ''' Draw Chord according ChordList[CHORD[3]]
        :TODO:: Kerning on 1-7, A-G, Sharp and Flat for FreeSerif
    '''
    Surface.set_source_rgb(0, 0, 0)
    Surface.move_to(105, 320)
    Surface.set_line_width(0.5)
    for j in range(10):
        for i in range(7):
            Surface.rel_line_to(0, 200)
            Surface.rel_move_to(384, -200)
        Surface.rel_move_to(-2688, 320)
    Surface.stroke()

    #
    for Chord in ChordList:
        Surface.set_font_size(100) #Temp
        Surface.move_to(Chord[3][0], Chord[3][1])# 2200, 3208 for temp
        Surface.show_text(Chord[0][0]) # show Root
        Surface.set_font_size(55)
        Surface.move_to(Chord[3][0]+45, Chord[3][1]+2)
        Surface.show_text(Chord[2]) # Show Quality


def CloseUp(Surface):
    Surface.show_page()
