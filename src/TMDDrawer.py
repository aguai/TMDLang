#!/usr/local/bin/python3
import cairocffi as cairo

A4 = [2480.0, 3508.0]
B4 = [2150.0, 3248.0]
A3 = [3508.0, 4960.0]
B3 = [3248.0, 4300.0]
PDFFileName = 'test.pdf'  # defult for debug
TestList = ['aguai ', chr(119056), chr(119057), '1m', 'Hanako']
FontSize = 50
currentSurface = cairo.Context(cairo.PDFSurface(PDFFileName, A4[0], A4[1]))
currentSurface.set_source_rgb(0, 0, 0)
currentSurface.set_line_width(1)


def DrawBasicLayout(CSF):
    for i in range(7):
        CSF.move_to(
            (A4[0] / 14) * ((2 * i) + 1), A4[1] / 18)
        for j in range(11):
            CSF.rel_move_to(0, A4[1] / 36)
            CSF.rel_line_to(0, A4[1] / 18)
    CSF.stroke()


def DrawChord(ThisPageChordList, CSF):
    CSF.move_to(0, 0)
    CSF.select_font_face("FreeSerif", cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_NORMAL)
    CSF.move_to(100, 100)
    CSF.set_font_size(60)
    for i in ThisPageChordList:
        CSF.show_text(i)
    CSF.show_page()


if __name__ == '__main__':
    DrawBasicLayout(currentSurface)
    DrawChord(TestList, currentSurface)
