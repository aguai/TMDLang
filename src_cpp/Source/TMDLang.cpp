#include "TMDLang.h"
#include <sstream>
#include <algorithm>

using namespace std;

namespace tmdlang
{
	/********************************************************
	Formatting
	********************************************************/

	std::ostream& operator<<(std::ostream& o, const Beat& value)
	{
		return o << '<' << value.count << '/' << value.node << '>';
	}

	std::ostream& operator<<(std::ostream& o, const Node& value)
	{
		o << value.name;
		switch (value.sharpFalls)
		{
		case SharpFalls::Sharp:
			o << '\'';
			break;
		case SharpFalls::Falls:
			o << ',';
			break;
		}

		if (value.octave > 0)
		{
			for (int i = 0; i < value.octave; i++) o << '^';
		}
		else if (value.octave < 0)
		{
			for (int i = 0; i < -value.octave; i++) o << '_';
		}
		return o;
	}

	std::ostream& operator<<(std::ostream& o, const Unit& value)
	{
		switch (value.type)
		{
		case UnitType::Node:
			return o << value.node;
		case UnitType::Chord:
			return o << '[' << value.chord << ']';
		default:
			return o << '-';
		}
	}

	std::ostream& operator<<(std::ostream& o, const Section& value)
	{
		o << "\t<" << value.nodeLength << "*>";
		int counter = 0;
		for (auto& unit : value.units)
		{
			if (counter % 16 == 0) o << endl << '\t';
			o << unit;
			counter++;
		}
		return o << endl << endl;
	}

	std::ostream& operator<<(std::ostream& o, const Paragraph& value)
	{
		o << value.name << ':' << value.instrument << "@|";
		if (value.start > 0)
		{
			o << '+' << value.start;
		}
		else
		{
			o << value.start;
		}
		o << "|{" << endl;

		for (auto& section : value.sections)
		{
			o << *section.get();
		}
		return o << '}' << endl << endl;
	}

	std::ostream& operator<<(std::ostream& o, const Order& value)
	{
		switch (value.type)
		{
		case OrderType::Relative:
			return o << "{?" << value.name << '}';
		case OrderType::Absolute:
			return o << "{?=" << value.name << '}';
		default:
			return o << value.name;
		}
	}

	std::ostream& operator<<(std::ostream& o, const Sheet& value)
	{
		o << "::SCORE::" << endl;
		o << "** " + value.name << " **" << endl;
		o << "!=" << value.speed << endl;
		o << "?=" << value.keySignature << endl;
		o << value.beat << endl;
		o << endl;

		for (auto& paragraph : value.paragraphs)
		{
			o << *paragraph.get();
		}

		int counter = 0;
		for (auto& order : value.orders)
		{
			o << order;
			if (++counter % 4 == 0) o << endl;
		}

		return o << "->#" << endl;
	}

	/********************************************************
	Parser
	********************************************************/
	
	string ltrim(string input, const char* ignores) {
		string s = input;
		s.erase(s.begin(), find_if(s.begin(), s.end(), [=](int ch) {
			return strchr(ignores, ch) != nullptr;
		}));
		return s;
	}

	string rtrim(string input, const char* ignores) {
		string s = input;
		s.erase(find_if(s.rbegin(), s.rend(), [=](int ch) {
			return strchr(ignores, ch) != nullptr;
		}).base(), s.end());
		return s;
	}

	struct CharReader
	{
		istream& i;
		char c;
		int row = 1;
		int column = 0;

		CharReader(istream& _i)
			:i(_i)
		{
		}

		bool GetChar()
		{
			if (i.eof()) return false;
			c = (char)i.get();
			if (c == '\n')
			{
				row++;
				column = 0;
			}
			else
			{
				column++;
			}
			return true;
		}

		bool Get(const char* ignores = "\r\n\t ")
		{
			if (ignores)
			{
				while (GetChar())
				{
					if (!strchr(ignores, c))
					{
						return true;
					}
				}
				return false;
			}
			else
			{
				return GetChar();
			}
		}

		string Read(const char until = 0, const char* ignores = "\r\n\t ")
		{
			if (!Get(ignores)) UnexpectedFileEnding();
			string result;
			stringstream ss;
			ss << c;
			while (GetChar())
			{
				if (until)
				{
					if (c == until)
					{
						return rtrim(ss.str(), ignores);
					}
				}
				else
				{
					if (strchr(ignores, c))
					{
						return ss.str();
					}
				}
				ss << c;
			}
			UnexpectedFileEnding();
		}

		void Ensure(const char* text)
		{
			auto reading = text;
			while (*reading++)
			{
				if (!Get()) UnexpectedFileEnding();
				if (reading[-1] != c) Error("Expect \"" + string(text) + "\" here.");
			}
		}

		void Error(string message)
		{
			stringstream ss;
			ss << "row: " << row << ", column: " << column << " message: " << message;
			throw ss.str();
		}

		void UnexpectedFileEnding()
		{
			Error("Unexpected file ending.");
		}
	};

	void Sheet::Read(std::istream& i)
	{
		CharReader cr(i);
		cr.Ensure("::SCORE::");

		while (cr.Get())
		{
			switch (cr.c)
			{
			case '*':
				cr.Ensure("*");
				name = cr.Read('*');
				cr.Ensure("*");
				break;
			case '!':
				{
					cr.Ensure("=");
					stringstream(cr.Read()) >> speed;
				}
				break;
			case '?':
				{
					cr.Ensure("=");
					keySignature = cr.Read();
				}
				break;
			case '<':
				{
					stringstream(cr.Read()) >> beat.count;
					cr.Ensure("/");
					stringstream(cr.Read()) >> beat.node;
					cr.Ensure(">");
				}
				break;
			case '-':
				while(true)
				{
					cr.Ensure(">");
					if (!cr.Get()) cr.UnexpectedFileEnding();
					switch (cr.c)
					{
					case '#':
						goto STOP_ORDER;
					case '{':
						{
							cr.Ensure("?");
							if (!cr.Get()) cr.UnexpectedFileEnding();
							switch (cr.c)
							{
							case '=':
								orders.push_back({ OrderType::Absolute,cr.Read('}') });
								break;
							default:
								{
									string name(1, cr.c);
									name += cr.Read('}');
									orders.push_back({ OrderType::Relative,name });
								}
								break;
							}
							cr.Ensure("-");
						}
						break;
					default:
						{
							string name(1, cr.c);
							name += cr.Read('-');
							orders.push_back({ OrderType::Name,name });
						}
						break;
					}
				}
				STOP_ORDER:
				break;
			default:
				break;
			}
		}
	}
}