package main

import	"strings"

func BarLineSriper(str string) string{ 
    return strings.Replace(str, "|", "", -1)
}
