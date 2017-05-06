package main

import (
	"fmt"
	"io/ioutil"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}
func main() {
	dat, err := ioutil.ReadFile("../example/creep.tmd")
	check(err)
	fmt.Print(string(dat))
}
