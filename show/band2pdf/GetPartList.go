package main

import (
	"regexp"
	"strings"
)

// GetPartList(GivenString string) []srting
// returns a List of Part ID Like "intro", "outro", "verse" ,etc...
// GivenString seems to be a whole file text
func GetPartList(GivenString string) []string {
	RePartSeq, _ := regexp.Compile("^->[^#]+")
	PartList := strings.Split(SpaceStriper(RePartSeq.FindString(GivenString)), "->")
	PartList = PartList[1 : len(PartList)-1]
	return PartList
	// I know I should call by pointer.
	// By now it's a python script which built in binary for me.
	// *REAL CODER* will do the optimize, which I am not!!!
}
