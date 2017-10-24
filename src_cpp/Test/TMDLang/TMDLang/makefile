.PHONY: all clean pre-build
.DEFAULT_GOAL := all

CPP_LINK=clang++ -std=c++14 -pthread -g $(CPP_COMPILE_OPTIONS) -o $@ $^
CPP_COMPILE=clang++ -std=c++14 -g $(CPP_COMPILE_OPTIONS) -o $@ -c $<

pre-build:
	if ! [ -d ./Debug ]; then mkdir ./Debug; fi

clean:
	if [ -d ./Debug ]; then rm -r ./Debug; fi

all:pre-build ./Debug/TMDLang

./Debug/TMDLang: ./Debug/Main.o ./Debug/TMDLang.o
	$(CPP_LINK)

./Debug/TMDLang.o: ../../../Source/TMDLang.cpp ../../../Source/TMDLang.h
	$(CPP_COMPILE)

./Debug/Main.o: ./Main.cpp ../../../Source/TMDLang.h
	$(CPP_COMPILE)

