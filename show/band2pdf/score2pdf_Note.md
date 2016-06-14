# 檢查副檔名
    
    .tmd

# 讀入檔案

    
    整體讀入應該是暫時沒有問題才對
    _~maybe first line first?~_


# 檢查檔案行爲

```    
    :!BAND-SCORE
    先找 :!   <=有沒有 peek() 可以用？
    再找 "\sBAND-SCORE\s+\n"
```

# 找歌曲 meta

```    
    歌名           :        "\s+**\s(?p:SONGNAME)\s**\s+\n"
    __VAR__        :        "^~:\s+__(?p:METANAME)__\s+\n"
```

這兩個要存下來塞到 .id3_tag 或 .mid, .cue, .lst 什麼的

```
    Printable Meta :        "^~:\s+\"(?p:PRINT_DATA)\"\s+\n"
```

這個應該只跟列印輸出有關
（有重複的不管都印出來就對了）


