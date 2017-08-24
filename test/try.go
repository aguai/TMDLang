package main

import "github.com/ungerik/go-cairo"

func main() {
	surface := cairo.NewPDFSurface("testpdf.pdf", 120, 220, cairo.PDF_VERSION_1_5)
	surface.SelectFontFace("FreeSerif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
	surface.SetFontSize(15)
	surface.SetSourceRGB(0, 0, 0)
	surface.MoveTo(10.0, 50.0)
	surface.ShowText("𝄐1m")
	surface.ShowPage()
	surface.SetLineWidth(2.5)
	surface.LineTo(66, 66)
	surface.Stroke()
	surface.MoveTo(10.0, 50.0)
	surface.ShowText("𝄆 𝄐2sus4 𝄇")
	surface.ShowPage()
	surface.Finish()
}
