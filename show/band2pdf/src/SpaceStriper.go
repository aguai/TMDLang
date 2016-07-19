package main

import (
	"strings"
	"unicode"
)

// Strip all the unnecessary char in the sting matched
// Thx StackOverflow
func SpaceStriper(str string) string {
	return strings.Map(func(x rune) rune {
		if unicode.IsSpace(x) {
			return -1
		}
		return x
	}, str)
}
