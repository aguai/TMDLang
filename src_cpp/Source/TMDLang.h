#pragma once

#include <iostream>
#include <memory>
#include <string>
#include <vector>

namespace tmdlang
{
	// <count/node>
	struct Beat
	{
		int						count = 4;
		int						node = 4;
	};

	enum class SharpFalls
	{
		Normal,
		Sharp,
		Falls,
	};

	// 1 ->    {octave:0  name:1 Normal}
	// 2'^^ -> {octave:2  name:2 Sharp }
	// 3,_ ->  {octave:-1 name:3 Falls }
	struct Node
	{
		SharpFalls				sharpFalls = SharpFalls::Normal;
		int						name = 0;
		int						octave = 0;
	};

	enum class UnitType
	{
		Node,		// 1
		Chord,		// [1]
		Copy,		// -
	};

	struct Unit
	{
		UnitType				type;
		Node					node;			// only available when type == Node
		std::string				chord;			// only available when type == Chord
	};

	struct UnitGroup
	{
		using List = std::vector<std::shared_ptr<UnitGroup>>;

		std::vector<Unit>		units;
		int						length = 1;

		virtual ~UnitGroup() = default;
	};

	struct Section
	{
		using List = std::vector<std::shared_ptr<Section>>;

		int						nodeLength = 4;	// <nodeLength*>
		UnitGroup::List			unitGroups;

		virtual ~Section() = default;
	};

	// name:instrument@|start|{ ... }
	struct Paragraph
	{
		using List = std::vector<std::shared_ptr<Paragraph> >;

		std::string				name;
		std::string				instrument;
		int						start = 0;
		Section::List			sections;

		virtual ~Paragraph() = default;
	};

	enum class OrderType
	{
		Name,		// intro
		Relative,	// {?+5}
		Absolute,	// {?=E,}
	};

	struct Order
	{
		OrderType				type;
		std::string				name;
	};

	struct Sheet
	{
		std::string				name;				// ** name **
		double					speed = 120;		// != speed
		std::string				keySignature = "C";	// ?= keySignature
		Beat					beat;				// <4/4>
		Paragraph::List			paragraphs;			//
		std::vector<Order>		orders;				// -> intro -> A -> {?+3} -> B ->#

		virtual ~Sheet() = default;

		void					Read(std::istream& i);	// report error by throwing std::string
	};

	extern std::ostream&		operator<<(std::ostream& o, const Beat& value);
	extern std::ostream&		operator<<(std::ostream& o, const Node& value);
	extern std::ostream&		operator<<(std::ostream& o, const Unit& value);
	extern std::ostream&		operator<<(std::ostream& o, const UnitGroup& value);
	extern std::ostream&		operator<<(std::ostream& o, const Section& value);
	extern std::ostream&		operator<<(std::ostream& o, const Paragraph& value);
	extern std::ostream&		operator<<(std::ostream& o, const Order& value);
	extern std::ostream&		operator<<(std::ostream& o, const Sheet& value);
}