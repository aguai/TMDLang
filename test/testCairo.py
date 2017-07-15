import cairo

'''
ps = cairo.PDFSurface("testpdf.pdf", 100, 100)
ct = cairo.Context(ps)

ct.set_source_rgb(0, 0, 0)
ct.select_font_face("FreeSerif", cairo.FONT_SLANT_NORMAL,
                    cairo.FONT_WEIGHT_NORMAL)
ct.set_font_size(20)
ct.move_to(50, 70)
ct.show_text(chr(119056) + chr(119057) + '2')
ct.copy_page()
ps.flush()
ct.move_to(50, 70)
ct.show_text(chr(119059) + chr(119058) + '3')
ct.show_page()
'''

ctx = cairo.Context(cairo.PDFSurface("testpdf.pdf", 2480.0, 3508.0))
ctx.set_font_size(30)
ctx.select_font_face("FreeSerif", cairo.FONT_SLANT_NORMAL,
                     cairo.FONT_WEIGHT_NORMAL)
ctx.move_to(300, 300)
ctx.line_to(300, 3208)
'''
ctx.show_text(chr(119056) + chr(119057) + '1ABCDEFGm')
ctx.show_page()  # 每次 show_page 會製作一個新頁面
ctx.move_to(100, 100)
ctx.show_text(chr(119056) + chr(119057) + '2maj')
ctx.move_to(100, 200)

glyphs = []
index = 0
for y in range(20):
    for x in range(35):
        glyphs.append((index, x * 100 + 100, y * 50 + 50))
        index += 1

ctx.show_glyphs(glyphs)
ctx.show_page()
