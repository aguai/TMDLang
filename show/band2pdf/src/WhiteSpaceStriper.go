package main

import (
	"strings"
	"unicode"
	"regexp"
)

// Strip all the unnecessary char in the sting matched
// Thx StackOverflow
func WhiteSpaceStriper(str string) string {
	return strings.Map(func(x rune) rune {	// difficult to decide if I should keep it anonymous?
		if unicode.IsSpace(x) {
			return -1
		}
		return x
	}, str)
}
