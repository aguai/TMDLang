import cairo


def main():

    ps = cairo.PDFSurface("pdffile.pdf", 504, 648)
    cr = cairo.Context(ps)

    cr.set_source_rgb(0, 0, 0)
    cr.select_font_face("FreeSerif", cairo.FONT_SLANT_NORMAL,
                        cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(40)
    cr.move_to(10, 50)
    cr.show_text(chr(119046) +'1 2 3 4 5' + chr(119047) )
    cr.set_line_width(11)
    cr.move_to(100, 100)
    cr.line_to(20, 300)

    cr.show_page()


if __name__ == "__main__":
    main()
