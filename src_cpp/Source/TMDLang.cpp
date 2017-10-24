#include "TMDLang.h"

using namespace std;

namespace tmdlang
{
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
}