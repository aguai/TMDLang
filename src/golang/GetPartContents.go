//
// \"(?P<PartName>[^\"]+)\"\:\"(?P<InstrumentName>[^\"]+)\"\@\[(?P<OnPosition>\S+)\]\{\s?\<(?P<TickBase>\d\d?)\*\>\s?(?P<PartContents>[^\}]+)\}
// finding out "PartName":"InstrumentName"@[OnPosition]{
// <TickBase*>
//  1233------|123|0---|---|
//  }
/*
I think I should write a formator afterward
*/
package main

//import (
//    "regexp"
//    "strings"
//)
//re := regexp.MustCompile(`\"(?P<PartName>[^\"]+)\":\"(?P<InstrumentName>[^\"]+)\"@\[(?P<OnPosition>[^\]]+)]{\<(?P<TickBase>\d\d?)\*\>(?P<PartContents>[^}]+)}`)
