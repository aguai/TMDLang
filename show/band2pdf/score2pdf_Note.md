1. 檢查副檔名

> ".tmd"

2. 讀入檔案

> 整體讀入應該是暫時沒有問題才對？ 
> ( _maybe first line first?_ )


3. 檢查檔案行爲

```    
    ":!BAND-SCORE"
    先找 ":!"
    再找 "\sBAND-SCORE\s+\n"
```

> _有沒有 peek() 可以用？_

4. 找歌曲 meta
```    
    歌名           :        "\s+**\s(?p:SONGNAME)\s**\s+\n"
    __VAR__        :        "^~:\s+__(?p:METANAME)__\s+=\"(?p:Name)\"\n"
```

> _這兩個要存下來塞到 .id3 或 .mid, .cue, .lst 什麼的_

```
    Printable Meta :        "^~\s+\"(?p:PRINT_DATA)\s+\"(?p:Name)\"\n"
```

> _這個應該只跟列印輸出有關（有重複的不管都印出來就對了）_

5. 找段落順序
re."->(gotPass1)->#"
[]=gotPass1.split("->") 
> _應該有更好的寫法，但是意思就是先把順序找出來，再把每個段落名稱塞進某個 Queue。_

