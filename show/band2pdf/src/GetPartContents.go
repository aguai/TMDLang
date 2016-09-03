//
// \"(?P<PartName>[^\"]+)\"\:\"(?P<InstrumentName>[^\"]+)\"\@\[(?P<OnPosition>\S+)\]\{\s?\<(?P<TickBase>\d\d?)\*\>\s?(?P<Contents>[^\}]+)\}
// finding out "PartName":"InstrumentName"@[OnPosition]{
// <TickBase*>
//    
// }