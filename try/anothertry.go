package main

import (
	"log"
	"os"

	"github.com/martine/gocairo/cairo"
)

func main() {
	log.Printf("cairo version %d/%s", cairo.Version(), cairo.VersionString())

	surf := cairo.ImageSurfaceCreate(cairo.FormatRGB24, 640, 480)
	cr := cairo.Create(surf.Surface)

	cr.SetSourceRGB(0, 0, 0)
	cr.Paint()

	cr.SetSourceRGB(1, 0, 0)
	cr.SelectFontFace("FreeSerif", cairo.FontSlantNormal, cairo.FontWeightNormal)
	cr.SetFontSize(50)
	cr.MoveTo(640/10, 480/2)
	cr.ShowText("𝄆 hello, world 𝄇")
	cr.MoveTo(640/10, 480/2+50)
	cr.SelectFontFace("Source Han Sans KR", cairo.FontSlantNormal, cairo.FontWeightNormal)
	cr.ShowText("본고딕")
	f, err := os.Create("example.png")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	err = surf.WriteToPNG(f)
	if err != nil {
		panic(err)
	}
}
