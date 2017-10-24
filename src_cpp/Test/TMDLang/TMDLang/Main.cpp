#include <iostream>
#include <fstream>
#include <string>
#include "../../../Source/TMDLang.h"

using namespace std;
using namespace tmdlang;

void Format(string filename)
{
	auto sheet = make_shared<Sheet>();
	{
		ifstream i(filename + ".tmd");
		sheet->Read(i);
	}
	{
		ofstream o(filename + ".formatted.tmd");
		o << *sheet.get();
	}
}

int main()
{
	Format("ChordOnly");
	Format("strangeChord");
	Format("creep");
	Format("三天三夜");
	return 0;
}