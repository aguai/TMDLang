############
x=re.findall(r"(?P<NoteEvent>[0-7]['|,]?[\^|_]?[\^|_]?\-*)", 
        '''0-----------5-6-1^-----2^1^------561^1^--1^-2^1^--------66666-56------71^2^2^2^2^2^-1^3^-2^------''')
yy=[]
for i in range(len(x)):
    yy.append(tuple([x[i].replace('-',''), x[i].count('-')+1]))
#############
for i in AllPartContent:
    if i[1]=='CHORD':
        print(i[0])
        ooxx=re.findall(r"\<(?P<Base>[12348][26]?)\*\>(?P<ChordString>[^<$]+)",i[3])[0]
        print('\tbase:\t'+ooxx[0])
        MatchChordWithLength=re.findall(r"(?P<ChordWithLength>\[[1-7][^\]]*\]\-*)", ooxx[1])
        print('\t\tchords:\n\t\t'+str(MatchChordWithLength))
        temp=[]
        for itr in range(len(MatchChordWithLength)):
            temp.append(MatchChordWithLength[itr].count('-')+1)
        print('\t\t'+str(temp))
        print('************************************************************')
