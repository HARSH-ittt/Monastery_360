"""
Sikkim Tourism Context Module
This module provides factual information about Sikkim to enhance chatbot responses.
"""

# Key tourist destinations in Sikkim
DESTINATIONS = {
    "gangtok": {
        "name": "Gangtok",
        "description": "Capital city of Sikkim, known for its cleanliness and scenic beauty",
        "attractions": ["MG Marg", "Enchey Monastery", "Ganesh Tok", "Hanuman Tok", "Tashi View Point"],
        "altitude": "1,650 meters (5,410 feet)",
        "best_time": "March to June and September to December"
    },
    "nathula": {
        "name": "Nathula Pass",
        "description": "Historic mountain pass on the Indo-China border",
        "attractions": ["Indo-China border trading post", "Scenic views", "Historic significance"],
        "altitude": "4,310 meters (14,140 feet)",
        "best_time": "May to October (closed on Mondays and Tuesdays)",
        "permit": "Special permit required for Indian nationals only"
    },
    "tsomgo": {
        "name": "Tsomgo Lake (Changu Lake)",
        "description": "Sacred high-altitude glacial lake",
        "attractions": ["Yak rides", "Scenic beauty", "Religious significance"],
        "altitude": "3,753 meters (12,313 feet)",
        "best_time": "May to September",
        "permit": "Protected area permit required"
    },
    "pelling": {
        "name": "Pelling",
        "description": "Small town offering spectacular views of Kanchenjunga",
        "attractions": ["Pemayangtse Monastery", "Rabdentse Ruins", "Kanchenjunga Falls", "Singshore Bridge"],
        "altitude": "2,150 meters (7,053 feet)",
        "best_time": "March to June and September to December"
    },
    "yuksom": {
        "name": "Yuksom",
        "description": "Historic town and base for Kanchenjunga treks",
        "attractions": ["Dubdi Monastery", "Kathok Lake", "Norbugang Park", "Trekking base"],
        "altitude": "1,780 meters (5,840 feet)",
        "best_time": "March to May and September to November"
    },
    "ravangla": {
        "name": "Ravangla",
        "description": "Small town known for Buddha Park and tea gardens",
        "attractions": ["Buddha Park", "Ralang Monastery", "Temi Tea Garden"],
        "altitude": "2,200 meters (7,217 feet)",
        "best_time": "March to June and September to December"
    }
}

# Major monasteries in Sikkim
MONASTERIES = {
    "rumtek": {
        "name": "Rumtek Monastery",
        "location": "Near Gangtok",
        "sect": "Karma Kagyu (Black Hat)",
        "significance": "Seat of the Karmapa Lama in exile, houses rare Buddhist artifacts",
        "founded": "Originally in 1740, rebuilt in 1960s"
    },
    "pemayangtse": {
        "name": "Pemayangtse Monastery",
        "location": "Near Pelling",
        "sect": "Nyingma",
        "significance": "One of the oldest and premier monasteries of Sikkim",
        "founded": "Late 17th century"
    },
    "tashiding": {
        "name": "Tashiding Monastery",
        "location": "Between Pelling and Yuksom",
        "sect": "Nyingma",
        "significance": "Considered one of the most sacred monasteries in Sikkim",
        "founded": "1641"
    },
    "enchey": {
        "name": "Enchey Monastery",
        "location": "Gangtok",
        "sect": "Nyingma",
        "significance": "Built on the site blessed by Lama Druptob Karpo",
        "founded": "1840s"
    }
}

# Major festivals of Sikkim
FESTIVALS = {
    "losar": {
        "name": "Losar",
        "timing": "February-March",
        "description": "Tibetan New Year celebration with prayers, dances, and feasts",
        "significance": "Marks the beginning of the Tibetan lunar calendar"
    },
    "saga_dawa": {
        "name": "Saga Dawa",
        "timing": "May-June (full moon)",
        "description": "Celebrates Buddha's birth, enlightenment, and parinirvana",
        "significance": "Most sacred Buddhist festival in Sikkim"
    },
    "drukpa_tseshi": {
        "name": "Drukpa Tseshi",
        "timing": "July-August",
        "description": "Commemorates Buddha's first sermon",
        "significance": "Day of turning the wheel of dharma"
    },
    "pang_lhabsol": {
        "name": "Pang Lhabsol",
        "timing": "August-September",
        "description": "Indigenous festival honoring Mount Kanchenjunga",
        "significance": "Unique to Sikkim, celebrates the mountain deity as protector"
    },
    "dasain": {
        "name": "Dasain (Dussehra)",
        "timing": "September-October",
        "description": "Hindu festival celebrating victory of good over evil",
        "significance": "Important for Sikkim's Nepali community"
    },
    "tihar": {
        "name": "Tihar (Diwali)",
        "timing": "October-November",
        "description": "Festival of lights celebrating various deities and animals",
        "significance": "Important for Sikkim's Nepali community"
    }
}

# Sikkim cuisine
CUISINE = {
    "momos": {
        "name": "Momos",
        "description": "Steamed or fried dumplings filled with meat or vegetables",
        "significance": "Most popular snack throughout Sikkim"
    },
    "thukpa": {
        "name": "Thukpa",
        "description": "Noodle soup with vegetables and meat",
        "significance": "Warming dish popular in colder regions"
    },
    "gundruk": {
        "name": "Gundruk",
        "description": "Fermented leafy green vegetable soup",
        "significance": "Traditional preservation technique and source of nutrients"
    },
    "sel_roti": {
        "name": "Sel Roti",
        "description": "Ring-shaped rice bread/doughnut, slightly sweet",
        "significance": "Festival food, especially during Tihar"
    },
    "chhurpi": {
        "name": "Chhurpi",
        "description": "Hard cheese made from yak or cow milk",
        "significance": "Traditional protein source that lasts long without refrigeration"
    },
    "phagshapa": {
        "name": "Phagshapa",
        "description": "Pork fat stew with radishes and dried chilies",
        "significance": "Traditional Bhutia dish"
    }
}

# Ethnic groups of Sikkim
ETHNIC_GROUPS = {
    "bhutia": {
        "name": "Bhutia",
        "origin": "Tibetan descent",
        "language": "Sikkimese (Bhutia)",
        "traditions": "Buddhist traditions, colorful festivals, traditional dress called Bakhu"
    },
    "lepcha": {
        "name": "Lepcha",
        "origin": "Indigenous to Sikkim",
        "language": "Lepcha (Róng)",
        "traditions": "Nature worship, rich folklore, traditional dress called Dum-prá"
    },
    "nepali": {
        "name": "Nepali",
        "origin": "Nepalese descent",
        "language": "Nepali",
        "traditions": "Hindu traditions, Dasain and Tihar festivals, diverse subgroups"
    },
    "limbu": {
        "name": "Limbu",
        "origin": "Indigenous to Eastern Himalayan region",
        "language": "Limbu",
        "traditions": "Yumaism (ancestral worship), Chasok Tangnam harvest festival"
    }
}

# Travel information
TRAVEL_INFO = {
    "best_time_to_visit": "March to June (spring) and September to December (autumn)",
    "monsoon": "June to September (heavy rainfall, landslides common)",
    "winter": "December to February (cold, some areas receive snowfall)",
    "permits": {
        "inner_line": "Required for certain areas like Nathula Pass, Tsomgo Lake, North Sikkim",
        "foreigner_restrictions": "Some border areas restricted for foreign nationals",
        "validity": "Usually valid for 15-30 days"
    },
    "transportation": {
        "nearest_airport": "Pakyong Airport (limited flights) or Bagdogra Airport (West Bengal)",
        "nearest_railway": "New Jalpaiguri (NJP) in West Bengal",
        "local_transport": "Shared jeeps, taxis, limited bus services"
    },
    "altitude_sickness": {
        "risk_areas": "North Sikkim, Nathula Pass, high-altitude treks",
        "prevention": "Proper acclimatization, stay hydrated, ascend slowly",
        "symptoms": "Headache, nausea, dizziness, fatigue"
    }
}

# Geography and climate
GEOGRAPHY = {
    "location": "Eastern Himalayas, bordered by Nepal, China (Tibet), Bhutan, and West Bengal",
    "area": "7,096 square kilometers (2,740 square miles)",
    "elevation_range": "300 to 8,586 meters (984 to 28,169 feet)",
    "major_peaks": {
        "kanchenjunga": {
            "name": "Kanchenjunga",
            "height": "8,586 meters (28,169 feet)",
            "rank": "Third highest mountain in the world",
            "significance": "Sacred to Sikkimese people, appears on state emblem"
        },
        "siniolchu": {
            "name": "Siniolchu",
            "height": "6,888 meters (22,598 feet)",
            "significance": "Known as the most beautiful mountain in the world"
        }
    },
    "rivers": ["Teesta", "Rangit", "Lachung", "Talung"],
    "climate_zones": {
        "subtropical": "Lower elevations up to 1,500 meters",
        "temperate": "1,500 to 3,500 meters",
        "alpine": "3,500 to 5,000 meters",
        "arctic": "Above 5,000 meters"
    }
}

# History of Sikkim
HISTORY = {
    "founding": {
        "year": "1642",
        "event": "Establishment of Namgyal Dynasty by Phuntsog Namgyal, first Chogyal (king)",
        "significance": "United various tribes under Buddhist monarchy"
    },
    "british_influence": {
        "period": "1817-1947",
        "events": "Treaty of Titalia (1817), British protectorate status",
        "significance": "Limited sovereignty, protection from external threats"
    },
    "indian_protectorate": {
        "year": "1950",
        "event": "Indo-Sikkim Treaty signed",
        "significance": "Sikkim became protectorate of independent India"
    },
    "statehood": {
        "year": "1975",
        "event": "Abolition of monarchy, referendum for Indian statehood",
        "significance": "Became 22nd state of India on April 26, 1975"
    }
}

def get_sikkim_facts():
    """Return a dictionary of all Sikkim facts for context enhancement"""
    return {
        "destinations": DESTINATIONS,
        "monasteries": MONASTERIES,
        "festivals": FESTIVALS,
        "cuisine": CUISINE,
        "ethnic_groups": ETHNIC_GROUPS,
        "travel_info": TRAVEL_INFO,
        "geography": GEOGRAPHY,
        "history": HISTORY
    }