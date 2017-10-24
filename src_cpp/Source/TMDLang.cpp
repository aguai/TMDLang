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

		string Read(bool skip = false, const char until = 0, const char* ignores = "\r\n\t ")
		{
			if (!Get(ignores)) UnexpectedFileEnding();
			string result;
			stringstream ss;
			if(!skip) ss << c;
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

		void Ensure(const char* text, const char* ignores = "\r\n\t ")
		{
			auto reading = text;
			while (*reading++)
			{
				while (true)
				{
					if (!Get()) UnexpectedFileEnding();
					if (!strchr(ignores, c)) break;
				}
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

		void UnexpectedChar(char ch = 0)
		{
			Error("Unexpected char: " + string(1, (ch ? ch : c)) + ".");
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
				name = cr.Read(true, '*');
				cr.Ensure("*");
				break;
			case '!':
				{
					cr.Ensure("=");
					stringstream(cr.Read(true)) >> speed;
				}
				break;
			case '?':
				{
					cr.Ensure("=");
					keySignature = cr.Read(true);
				}
				break;
			case '<':
				{
					stringstream(cr.Read(true)) >> beat.count;
					cr.Ensure("/");
					stringstream(cr.Read(true)) >> beat.node;
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
								orders.push_back({ OrderType::Absolute,cr.Read(true, '}') });
								break;
							default:
								orders.push_back({ OrderType::Relative,cr.Read(false,'}') });
								break;
							}
							cr.Ensure("-");
						}
						break;
					default:
						orders.push_back({ OrderType::Name,cr.Read(false,'-') });
						break;
					}
				}
				STOP_ORDER:
				break;
			default:
				{
					auto paragraph = make_shared<Paragraph>();
					paragraphs.push_back(paragraph);
					paragraph->name = cr.Read(false, ':');
					paragraph->instrument = cr.Read(true, '@');
					cr.Ensure("|");
					stringstream(cr.Read(false, '|')) >> paragraph->start;
					cr.Ensure("{");

					if (!cr.Get()) cr.UnexpectedFileEnding();
					while (true)
					{
						switch (cr.c)
						{
						case '<':
							{
								auto section = make_shared<Section>();
								paragraph->sections.push_back(section);

								stringstream(cr.Read(true, '*')) >> section->nodeLength;
								cr.Ensure(">");

								if (!cr.Get("\r\n\t |")) cr.UnexpectedFileEnding();
								while (true)
								{
									if (cr.c == '<' || cr.c == '}')break;
									switch (cr.c)
									{
									case '-':
										section->units.push_back({ UnitType::Copy });
										if (!cr.Get("\r\n\t |")) cr.UnexpectedFileEnding();
										break;
									case '[':
										section->units.push_back({ UnitType::Chord,{},cr.Read(true,']') });
										if (!cr.Get("\r\n\t |")) cr.UnexpectedFileEnding();
										break;
									default:
										{
											Node node;
											if (!('1' <= cr.c && cr.c <= '7'))
											{
												cr.UnexpectedChar();
											}
											node.name = cr.c - '1';

											while (true)
											{
												if (!cr.Get("\r\n\t |")) cr.UnexpectedFileEnding();
												if (cr.c == '\'')
												{
													node.sharpFalls = SharpFalls::Sharp;
												}
												else if (cr.c == ',')
												{
													node.sharpFalls = SharpFalls::Falls;
												}
												else if (cr.c == ',')
												{
													node.sharpFalls = SharpFalls::Falls;
												}
												else if (cr.c == '^')
												{
													node.octave++;
												}
												else if (cr.c == '_')
												{
													node.octave--;
												}
												else
												{
													section->units.push_back({ UnitType::Node,node });
													break;
												}
											}
										}
										break;
									}
								}
							}
							break;
						case '}':
							goto STOP_PARAGRAPH;
						default:
							cr.UnexpectedChar();
						}
					}
				}
				STOP_PARAGRAPH:
				break;
			}
		}
	}
}