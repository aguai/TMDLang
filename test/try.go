package main

import "github.com/ungerik/go-cairo"

func main() {
	surface := cairo.NewPDFSurface("testpdf.pdf", 120, 220, cairo.PDF_VERSION_1_5)
	surface.SelectFontFace("FreeSerif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
	surface.SetFontSize(15)
	surface.SetSourceRGB(0, 0, 0)
	surface.MoveTo(10.0, 50.0)
	surface.ShowText("𝄐1m")
	surface.CopyPage()
	surface.ShowPage()
	surface.Finish()
}
