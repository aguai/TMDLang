package main

import (
	"fmt"
	"regexp"
)

func main() {
	var re = regexp.MustCompile(`(\<(?P<base>1|2|4|8|16|32)\*\>)(?P<this_Contents>[^\<]+)`)
	var str = `<4*>[1]-[1sus4][1Maj7][3]-
	[3sus4][3][4]-[4/2][4][4m]-[6,][7,]
<1*>[1]-[1/5]-[1]-[1][1]
<16*>[1][1'][2]`

	/*
		for i, match := range re.FindAllString(str, -1) {
			fmt.Println(match, "found at index", i)
		}
	*/
	match2 := re.FindStringSubmatch(str)
	result := make(map[string]string)
	for i, name := range re.SubexpNames() {
		if i != 0 {
			result[name] = match2[i]
		}
	}
	fmt.Printf("%s %s\n", result["base"], result["thid_Contents"])
}
