# -*- coding: utf8 -*-
import cairo

A4=[595.0, 842.0] # @ 300DPI
#def Page(NAME, TYPE, Size):
    # NAME: Song Name (with page#?)
    # TYPE: {PDF, SVG}
    # Size: {A3, A4, B4, B3}
#    if   TYPE == 'PDF':
#        return cairo.Context(cairo.PDFSurface(NAME+'.pdf', Size[0], Size[1]))
#    elif TYPE == 'SVG':
#        return cairo.Context(cairo.SVGSurface(NAME+'.svg', Size[0], Size[1]))

    
def ChordDrawer(NAME, TYPE, Size ,ChordList) :
    # NAME: Song Name (with page#?)
    # TYPE: {PDF, SVG}
    # Size: {A3, A4, B4, B3}
    #
    # Surface:  cairo.Surface 
    # Root:     char : with or without sup Flat or Sharp
    # Bass:     char : under a slash '/' ('' for no Alternative bass note to draw)
    # Quality:  str  : Interval included ex: symbol like +, Δ(Maj7), o(dim), alt, sus, etc. 
    # Position: tuple: (x,y): position to draw this Chord 
    Surface.set_source_rgb(0, 0, 0)
    Surface.select_font_face("FreeSerif", cairo.FONT_SLANT_NORMAL,
        cairo.FONT_WEIGHT_NORMAL)
    Surface.set_font_size(20)
    Surface.move_to(Position[0], Position[1])# 2200, 3208 for temp
    Surface.show_text(Root)
    Surface.set_font_size(11)
    Surface.move_to(Position[0]+10, Position[1])
    Surface.show_text(Quality)
    Surface.show_page()

def CloseUp(Surface):
    Surface.show_page()