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

	std::ostream& operator<<(std::ostream& o, const UnitGroup& value)
	{
		if (value.units.size() == 1 && value.length == 1)
		{
			o << value.units[0];
		}
		else
		{
			o << "(";
			for (auto& unit : value.units)
			{
				o << unit;
			}
			o << ")%(";
			for (int i = 0; i < value.length; i++)
			{
				o << "-";
			}
			o << ")";
		}
		return o;
	}

	std::ostream& operator<<(std::ostream& o, const Section& value)
	{
		o << "\t<" << value.nodeLength << "*>";
		int counter = 0;
		for (auto& unitGroup : value.unitGroups)
		{
			if (counter % 8 == 0 || counter >= 8)
			{
				o << endl << '\t';
				counter = 0;
			}
			o << *unitGroup.get() << ' ';
			counter += unitGroup->length;
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
			o << "-> " << order << " ";
			if (++counter % 4 == 0) o << endl;
		}

		return o << "->#" << endl;
	}

	/********************************************************
	Parser
	********************************************************/
	
	string ltrim(string input, const char* ignores) {
		string s = input;
		auto it = find_if(s.begin(), s.end(), [=](int ch) {
			return strchr(ignores, ch) == nullptr;
		});
		if (it == s.end()) return s;
		s.erase(s.begin(), it);
		return s;
	}

	string rtrim(string input, const char* ignores) {
		string s = input;
		auto it = find_if(s.rbegin(), s.rend(), [=](int ch) {
			return strchr(ignores, ch) == nullptr;
		});
		if (it == s.rend()) return s;
		s.erase(it.base(), s.end());
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
			c = (char)i.get();
			if (i.eof()) return false;
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
						if (c == '/')
						{
							if (!GetChar()) UnexpectedFileEnding();
							if (c != '*') Error("Wrong comment format.");

							bool waitingCommentEnd = false;
							while (GetChar())
							{
								if (c == '*')
								{
									waitingCommentEnd = true;
								}
								else if (c == '/')
								{
									if (waitingCommentEnd)
									{
										goto STOP_COMMENT;
									}
								}
								else
								{
									waitingCommentEnd = false;
								}
							}
							UnexpectedFileEnding();
						STOP_COMMENT:
							continue;
						}
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

		void EnsureGet(const char* ignores = "\r\n\t ")
		{
			if (!Get(ignores)) UnexpectedFileEnding();
		}

		string ReadNullable(bool skip = false, const char until = 0, const char* ignores = "\r\n\t ")
		{
			string result;
			stringstream ss;

			if (skip)
			{
				Get(ignores);
			}

			while (true)
			{
				if (until)
				{
					if (c == until)
					{
						return ltrim(rtrim(ss.str(), ignores), ignores);
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
				GetChar();
			}
			UnexpectedFileEnding();
		}

		string Read(bool skip = false, const char until = 0, const char* ignores = "\r\n\t ")
		{
			string s = ReadNullable(skip, until, ignores);
			if (s == "")
			{
				Error("Unexpected empty string.");
			}
			return s;
		}

		void Ensure(const char* text, const char* ignores = "\r\n\t ")
		{
			auto reading = text;
			while (*reading++)
			{
				while (true)
				{
					EnsureGet();
					if (!strchr(ignores, c)) break;
				}
				if (reading[-1] != c) Error("Expect \"" + string(text) + "\" here.");
			}
		}

		void Error(string message)
		{
			stringstream ss;
			ss << "row: " << row << ", column: " << column << " message: " << message;
			string s = ss.str();
#ifdef _DEBUG
			cout << s << endl;
#endif
			throw s;
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

	Unit ReadUnitLookedAhead(CharReader& cr)
	{
		switch (cr.c)
		{
		case '-':
			{
				Unit unit = { UnitType::Copy };
				cr.EnsureGet("\r\n\t |");
				return unit;
			}
		case '[':
			{
				Unit unit = { UnitType::Chord,{},cr.Read(true,']') };
				cr.EnsureGet("\r\n\t |");
				return unit;
			}
		default:
			{
				Node node;
				if (!('1' <= cr.c && cr.c <= '7'))
				{
					cr.UnexpectedChar();
				}
				node.name = cr.c - '0';

				while (true)
				{
					cr.EnsureGet("\r\n\t |");
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
						return{ UnitType::Node,node };
					}
				}
			}
			break;
		}
	}

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
					stringstream(cr.Read(true, '/')) >> beat.count;
					stringstream(cr.Read(true, '>')) >> beat.node;
				}
				break;
			case '-':
				while(true)
				{
					cr.Ensure(">");
					cr.EnsureGet();
					switch (cr.c)
					{
					case '#':
						goto STOP_ORDER;
					case '{':
						{
							cr.Ensure("?");
							cr.EnsureGet();
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
					paragraph->name = cr.ReadNullable(false, ':');
					paragraph->instrument = cr.Read(true, '@');

					cr.EnsureGet();
					if (cr.c == '|')
					{
						stringstream(cr.Read(true, '|')) >> paragraph->start;
						cr.Ensure("{");
					}
					else if (cr.c != '{')
					{
						cr.UnexpectedChar();
					}

					cr.EnsureGet();
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

								cr.EnsureGet("\r\n\t |");
								while (true)
								{
									if (cr.c == '<' || cr.c == '}')break;

									auto unitGroup = make_shared<UnitGroup>();
									section->unitGroups.push_back(unitGroup);
									if (cr.c == '(')
									{
										cr.EnsureGet("\r\n\t |");
										while (true)
										{
											if (cr.c == ')')break;
											unitGroup->units.push_back(ReadUnitLookedAhead(cr));
										}
										cr.Ensure("%(");
										unitGroup->length = 0;
										while (true)
										{
											cr.EnsureGet();
											if (cr.c == ')') break;
											else if (cr.c == '-') unitGroup->length++;
											else cr.UnexpectedChar();
										}
										cr.EnsureGet("\r\n\t |");
									}
									else
									{
										unitGroup->units.push_back(ReadUnitLookedAhead(cr));
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