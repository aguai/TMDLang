package main

import (
	"strings"
	"unicode"
	"regexp"
)

// Strip all the unnecessary char in the sting matched
// Thx StackOverflow
func UselessCharStriper(str string) string {
	return strings.Map(func(x rune) rune {
		if unicode.IsSpace(x) {
			return -1
		}
		if 
		return x
	}, str)
}
