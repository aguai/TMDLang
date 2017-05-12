import cairo

A4 = [2480.0, 3508.0]
B4 = [2150.0, 3248.0]
A3 = [3508.0, 4960.0]
B3 = [3248.0, 4300.0]
PDFFileName = 'test.pdf'
FontSize = 0
currentSurface = cairo.Context(cairo.PDFSurface(PDFFileName, A4[0], A4[1]))
currentSurface.set_source_rgb(0, 0, 0)
currentSurface.set_line_width(1)


def basicLayout():
    for i in range(7):
        currentSurface.move_to(
            (A4[0] / 14) * ((2 * i) + 1),
            A4[1] / 18)
        for j in range(11):
            currentSurface.rel_move_to(0, A4[1] / 36)
            currentSurface.rel_line_to(0, A4[1] / 18)

        currentSurface.stroke()


if __name__ == '__main__':
    basicLayout()
    currentSurface.show_page()
