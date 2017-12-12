# TMDLang

Timebase Mark Down Language

## description

a markup language for sequent event like **band style music score** or **show rundown sheet**

## 概述（中文）

以類似 Markdown Languange 的標記語法建立依時序進行的事件流程表格諸如 **樂隊形式級數樂譜** 或 **活動節目流程**

### for macOS

1. in order to use charactors like 🎝 , 𝆒 , 𝄋, 𝄌,etc. [FreeSerif](http://ftp.gnu.org/gnu/freefont/freefont-ttf-20120503.zip) and [Hanazono](http://fonts.jp/hanazono/) must be install separately.

2. libcairo should be rebuild with these flags :
    ```
    ./configure --enable-quartz=no --enable-quartz-font=no --enable-quartz-image=no
    ```
    (bug has been fix and push into mainstream)

### for macOS(中文)

1. 請自行安裝 [FreeSerif](http://ftp.gnu.org/gnu/freefont/freefont-ttf-20120503.zip) 及 [花園明朝](http://fonts.jp/hanazono/) 兩組字體以俾顯示 🎝 , 𝆒 , 𝄋, 𝄌 等字體。

2. ~~libcairo 需要以以下 flags 重新編譯:~~
    ```bash
    # ./configure --enable-quartz=no --enable-quartz-font=no --enable-quartz-image=no
    ```
    (bug has been fix and push into mainstream)

