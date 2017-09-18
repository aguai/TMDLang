package main

import (
	"fmt"
	"reflect"
	"regexp"
)

var path = "articles/anya/visuddhimagga/visuddhimagga-chap01%zh.rst"

func main() {
	pattern := `articles/(?P<urlpath>[-a-zA-Z0-9/]*)/(?P<slug>[-a-zA-Z0-9]*)%(?P<lang>[_a-zA-Z]{2,5})\.rst`
	pathMetadata := regexp.MustCompile(pattern)

	matches := pathMetadata.FindStringSubmatch(path)
	names := pathMetadata.SubexpNames()
	fmt.Printf("%s:\n\t%s\n", names, reflect.TypeOf(names).Kind())
	fmt.Printf("%s:\n\t%s\n", matches, reflect.TypeOf(matches).Kind())

	for i, match := range matches {
		if i != 0 {
			fmt.Println(names[i], match)
		}
	}
}
