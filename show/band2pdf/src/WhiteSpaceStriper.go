package main

import (
	"strings"
	"unicode"
	"regexp"
)

// Strip all the unnecessary char in the sting matched
// Thx StackOverflow
func WhiteSpaceStriper(str string) string {
	BarStriped:= strings.Replace(str, "|", "", -1)
	return strings.Map(func(x rune) rune {	// difficult to decide if I should keep it anonymous?
		if unicode.IsSpace(x) {
			return -1
		}
		return x
	}, BarStriped)

}
