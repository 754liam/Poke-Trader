# Pre-cached Pokemon card data for instant search results without API calls
# Python standard library

PIKACHU_CARDS = [
    {
        "id": "base1-58",
        "name": "Pikachu",
        "set": {"id": "base1", "name": "Base", "series": "Base", "releaseDate": "1999/01/09"},
        "images": {"small": "https://images.pokemontcg.io/base1/58.png", "large": "https://images.pokemontcg.io/base1/58_hires.png"}
    },
    {
        "id": "cel25-5",
        "name": "Pikachu",
        "set": {"id": "cel25", "name": "Celebrations", "series": "Sword & Shield", "releaseDate": "2021/10/08"},
        "images": {"small": "https://images.pokemontcg.io/cel25/5.png", "large": "https://images.pokemontcg.io/cel25/5_hires.png"}
    },
    {
        "id": "swsh4-43",
        "name": "Pikachu V",
        "set": {"id": "swsh4", "name": "Vivid Voltage", "series": "Sword & Shield", "releaseDate": "2020/11/13"},
        "images": {"small": "https://images.pokemontcg.io/swsh4/43.png", "large": "https://images.pokemontcg.io/swsh4/43_hires.png"}
    },
    {
        "id": "swsh4-44",
        "name": "Pikachu VMAX",
        "set": {"id": "swsh4", "name": "Vivid Voltage", "series": "Sword & Shield", "releaseDate": "2020/11/13"},
        "images": {"small": "https://images.pokemontcg.io/swsh4/44.png", "large": "https://images.pokemontcg.io/swsh4/44_hires.png"}
    },
    {
        "id": "sv2-63",
        "name": "Pikachu ex",
        "set": {"id": "sv2", "name": "Paldea Evolved", "series": "Scarlet & Violet", "releaseDate": "2023/06/09"},
        "images": {"small": "https://images.pokemontcg.io/sv2/63.png", "large": "https://images.pokemontcg.io/sv2/63_hires.png"}
    },
    {
        "id": "sv8-57",
        "name": "Pikachu ex",
        "set": {"id": "sv8", "name": "Surging Sparks", "series": "Scarlet & Violet", "releaseDate": "2024/11/08"},
        "images": {"small": "https://images.pokemontcg.io/sv8/57.png", "large": "https://images.pokemontcg.io/sv8/57_hires.png"}
    },
    {
        "id": "xy12-35",
        "name": "Pikachu",
        "set": {"id": "xy12", "name": "Evolutions", "series": "XY", "releaseDate": "2016/11/02"},
        "images": {"small": "https://images.pokemontcg.io/xy12/35.png", "large": "https://images.pokemontcg.io/xy12/35_hires.png"}
    },
    {
        "id": "sm9-33",
        "name": "Pikachu & Zekrom-GX",
        "set": {"id": "sm9", "name": "Team Up", "series": "Sun & Moon", "releaseDate": "2019/02/01"},
        "images": {"small": "https://images.pokemontcg.io/sm9/33.png", "large": "https://images.pokemontcg.io/sm9/33_hires.png"}
    },
    {
        "id": "det1-10",
        "name": "Detective Pikachu",
        "set": {"id": "det1", "name": "Detective Pikachu", "series": "Sun & Moon", "releaseDate": "2019/04/05"},
        "images": {"small": "https://images.pokemontcg.io/det1/10.png", "large": "https://images.pokemontcg.io/det1/10_hires.png"}
    },
    {
        "id": "sv3pt5-25",
        "name": "Pikachu",
        "set": {"id": "sv3pt5", "name": "151", "series": "Scarlet & Violet", "releaseDate": "2023/09/22"},
        "images": {"small": "https://images.pokemontcg.io/sv3pt5/25.png", "large": "https://images.pokemontcg.io/sv3pt5/25_hires.png"}
    },
    {
        "id": "g1-26",
        "name": "Pikachu",
        "set": {"id": "g1", "name": "Generations", "series": "XY", "releaseDate": "2016/02/22"},
        "images": {"small": "https://images.pokemontcg.io/g1/26.png", "large": "https://images.pokemontcg.io/g1/26_hires.png"}
    },
    {
        "id": "basep-1",
        "name": "Pikachu",
        "set": {"id": "basep", "name": "Wizards Black Star Promos", "series": "Base", "releaseDate": "1999/07/01"},
        "images": {"small": "https://images.pokemontcg.io/basep/1.png", "large": "https://images.pokemontcg.io/basep/1_hires.png"}
    },
    {
        "id": "swsh1-65",
        "name": "Pikachu",
        "set": {"id": "swsh1", "name": "Sword & Shield", "series": "Sword & Shield", "releaseDate": "2020/02/07"},
        "images": {"small": "https://images.pokemontcg.io/swsh1/65.png", "large": "https://images.pokemontcg.io/swsh1/65_hires.png"}
    },
    {
        "id": "pgo-28",
        "name": "Pikachu",
        "set": {"id": "pgo", "name": "Pokémon GO", "series": "Sword & Shield", "releaseDate": "2022/07/01"},
        "images": {"small": "https://images.pokemontcg.io/pgo/28.png", "large": "https://images.pokemontcg.io/pgo/28_hires.png"}
    },
    {
        "id": "neo1-70",
        "name": "Pikachu",
        "set": {"id": "neo1", "name": "Neo Genesis", "series": "Neo", "releaseDate": "2000/12/16"},
        "images": {"small": "https://images.pokemontcg.io/neo1/70.png", "large": "https://images.pokemontcg.io/neo1/70_hires.png"}
    }
]

MEOWSCARADA_CARDS = [
    {
        "id": "sv1-15",
        "name": "Meowscarada",
        "set": {"id": "sv1", "name": "Scarlet & Violet", "series": "Scarlet & Violet", "releaseDate": "2023/03/31"},
        "images": {"small": "https://images.pokemontcg.io/sv1/15.png", "large": "https://images.pokemontcg.io/sv1/15_hires.png"}
    },
    {
        "id": "sv2-15",
        "name": "Meowscarada ex",
        "set": {"id": "sv2", "name": "Paldea Evolved", "series": "Scarlet & Violet", "releaseDate": "2023/06/09"},
        "images": {"small": "https://images.pokemontcg.io/sv2/15.png", "large": "https://images.pokemontcg.io/sv2/15_hires.png"}
    },
    {
        "id": "sv2-256",
        "name": "Meowscarada ex",
        "set": {"id": "sv2", "name": "Paldea Evolved", "series": "Scarlet & Violet", "releaseDate": "2023/06/09"},
        "images": {"small": "https://images.pokemontcg.io/sv2/256.png", "large": "https://images.pokemontcg.io/sv2/256_hires.png"}
    },
    {
        "id": "sv2-231",
        "name": "Meowscarada ex",
        "set": {"id": "sv2", "name": "Paldea Evolved", "series": "Scarlet & Violet", "releaseDate": "2023/06/09"},
        "images": {"small": "https://images.pokemontcg.io/sv2/231.png", "large": "https://images.pokemontcg.io/sv2/231_hires.png"}
    },
    {
        "id": "sv2-271",
        "name": "Meowscarada ex",
        "set": {"id": "sv2", "name": "Paldea Evolved", "series": "Scarlet & Violet", "releaseDate": "2023/06/09"},
        "images": {"small": "https://images.pokemontcg.io/sv2/271.png", "large": "https://images.pokemontcg.io/sv2/271_hires.png"}
    },
    {
        "id": "svp-33",
        "name": "Meowscarada ex",
        "set": {"id": "svp", "name": "Scarlet & Violet Black Star Promos", "series": "Scarlet & Violet", "releaseDate": "2023/01/01"},
        "images": {"small": "https://images.pokemontcg.io/svp/33.png", "large": "https://images.pokemontcg.io/svp/33_hires.png"}
    },
    {
        "id": "svp-78",
        "name": "Meowscarada ex",
        "set": {"id": "svp", "name": "Scarlet & Violet Black Star Promos", "series": "Scarlet & Violet", "releaseDate": "2023/01/01"},
        "images": {"small": "https://images.pokemontcg.io/svp/78.png", "large": "https://images.pokemontcg.io/svp/78_hires.png"}
    },
    {
        "id": "sv9-18",
        "name": "Meowscarada",
        "set": {"id": "sv9", "name": "Journey Together", "series": "Scarlet & Violet", "releaseDate": "2025/03/28"},
        "images": {"small": "https://images.pokemontcg.io/sv9/18.png", "large": "https://images.pokemontcg.io/sv9/18_hires.png"}
    }
]

MEWTWO_CARDS = [
    {
        "id": "base1-10",
        "name": "Mewtwo",
        "set": {"id": "base1", "name": "Base", "series": "Base", "releaseDate": "1999/01/09"},
        "images": {"small": "https://images.pokemontcg.io/base1/10.png", "large": "https://images.pokemontcg.io/base1/10_hires.png"}
    },
    {
        "id": "det1-12",
        "name": "Mewtwo",
        "set": {"id": "det1", "name": "Detective Pikachu", "series": "Sun & Moon", "releaseDate": "2019/04/05"},
        "images": {"small": "https://images.pokemontcg.io/det1/12.png", "large": "https://images.pokemontcg.io/det1/12_hires.png"}
    },
    {
        "id": "sm11-71",
        "name": "Mewtwo & Mew-GX",
        "set": {"id": "sm11", "name": "Unified Minds", "series": "Sun & Moon", "releaseDate": "2019/08/02"},
        "images": {"small": "https://images.pokemontcg.io/sm11/71.png", "large": "https://images.pokemontcg.io/sm11/71_hires.png"}
    },
    {
        "id": "sm35-39",
        "name": "Mewtwo-GX",
        "set": {"id": "sm35", "name": "Shining Legends", "series": "Sun & Moon", "releaseDate": "2017/10/06"},
        "images": {"small": "https://images.pokemontcg.io/sm35/39.png", "large": "https://images.pokemontcg.io/sm35/39_hires.png"}
    },
    {
        "id": "pgo-30",
        "name": "Mewtwo V",
        "set": {"id": "pgo", "name": "Pokémon GO", "series": "Sword & Shield", "releaseDate": "2022/07/01"},
        "images": {"small": "https://images.pokemontcg.io/pgo/30.png", "large": "https://images.pokemontcg.io/pgo/30_hires.png"}
    },
    {
        "id": "pgo-31",
        "name": "Mewtwo VSTAR",
        "set": {"id": "pgo", "name": "Pokémon GO", "series": "Sword & Shield", "releaseDate": "2022/07/01"},
        "images": {"small": "https://images.pokemontcg.io/pgo/31.png", "large": "https://images.pokemontcg.io/pgo/31_hires.png"}
    },
    {
        "id": "sv4-58",
        "name": "Mewtwo ex",
        "set": {"id": "sv4", "name": "Paradox Rift", "series": "Scarlet & Violet", "releaseDate": "2023/11/03"},
        "images": {"small": "https://images.pokemontcg.io/sv4/58.png", "large": "https://images.pokemontcg.io/sv4/58_hires.png"}
    },
    {
        "id": "sv3pt5-150",
        "name": "Mewtwo",
        "set": {"id": "sv3pt5", "name": "151", "series": "Scarlet & Violet", "releaseDate": "2023/09/22"},
        "images": {"small": "https://images.pokemontcg.io/sv3pt5/150.png", "large": "https://images.pokemontcg.io/sv3pt5/150_hires.png"}
    },
    {
        "id": "xy12-51",
        "name": "Mewtwo",
        "set": {"id": "xy12", "name": "Evolutions", "series": "XY", "releaseDate": "2016/11/02"},
        "images": {"small": "https://images.pokemontcg.io/xy12/51.png", "large": "https://images.pokemontcg.io/xy12/51_hires.png"}
    },
    {
        "id": "bw4-54",
        "name": "Mewtwo-EX",
        "set": {"id": "bw4", "name": "Next Destinies", "series": "Black & White", "releaseDate": "2012/02/08"},
        "images": {"small": "https://images.pokemontcg.io/bw4/54.png", "large": "https://images.pokemontcg.io/bw4/54_hires.png"}
    },
    {
        "id": "swsh12pt5-59",
        "name": "Mewtwo",
        "set": {"id": "swsh12pt5", "name": "Crown Zenith", "series": "Sword & Shield", "releaseDate": "2023/01/20"},
        "images": {"small": "https://images.pokemontcg.io/swsh12pt5/59.png", "large": "https://images.pokemontcg.io/swsh12pt5/59_hires.png"}
    },
    {
        "id": "swsh9-56",
        "name": "Mewtwo",
        "set": {"id": "swsh9", "name": "Brilliant Stars", "series": "Sword & Shield", "releaseDate": "2022/02/25"},
        "images": {"small": "https://images.pokemontcg.io/swsh9/56.png", "large": "https://images.pokemontcg.io/swsh9/56_hires.png"}
    },
    {
        "id": "sv10-81",
        "name": "Team Rocket's Mewtwo ex",
        "set": {"id": "sv10", "name": "Destined Rivals", "series": "Scarlet & Violet", "releaseDate": "2025/05/30"},
        "images": {"small": "https://images.pokemontcg.io/sv10/81.png", "large": "https://images.pokemontcg.io/sv10/81_hires.png"}
    },
    {
        "id": "basep-3",
        "name": "Mewtwo",
        "set": {"id": "basep", "name": "Wizards Black Star Promos", "series": "Base", "releaseDate": "1999/07/01"},
        "images": {"small": "https://images.pokemontcg.io/basep/3.png", "large": "https://images.pokemontcg.io/basep/3_hires.png"}
    },
    {
        "id": "sm115-31",
        "name": "Mewtwo-GX",
        "set": {"id": "sm115", "name": "Hidden Fates", "series": "Sun & Moon", "releaseDate": "2019/08/23"},
        "images": {"small": "https://images.pokemontcg.io/sm115/31.png", "large": "https://images.pokemontcg.io/sm115/31_hires.png"}
    }
]

CHARIZARD_CARDS = [
    {
        "id": "base1-4",
        "name": "Charizard",
        "set": {"id": "base1", "name": "Base", "series": "Base", "releaseDate": "1999/01/09"},
        "images": {"small": "https://images.pokemontcg.io/base1/4.png", "large": "https://images.pokemontcg.io/base1/4_hires.png"}
    },
    {
        "id": "gym2-2",
        "name": "Blaine's Charizard",
        "set": {"id": "gym2", "name": "Gym Challenge", "series": "Gym", "releaseDate": "2000/10/16"},
        "images": {"small": "https://images.pokemontcg.io/gym2/2.png", "large": "https://images.pokemontcg.io/gym2/2_hires.png"}
    },
    {
        "id": "xy12-11",
        "name": "Charizard",
        "set": {"id": "xy12", "name": "Evolutions", "series": "XY", "releaseDate": "2016/11/02"},
        "images": {"small": "https://images.pokemontcg.io/xy12/11.png", "large": "https://images.pokemontcg.io/xy12/11_hires.png"}
    },
    {
        "id": "swsh3-20",
        "name": "Charizard VMAX",
        "set": {"id": "swsh3", "name": "Darkness Ablaze", "series": "Sword & Shield", "releaseDate": "2020/08/14"},
        "images": {"small": "https://images.pokemontcg.io/swsh3/20.png", "large": "https://images.pokemontcg.io/swsh3/20_hires.png"}
    },
    {
        "id": "swsh45sv-SV107",
        "name": "Charizard VMAX",
        "set": {"id": "swsh45sv", "name": "Shining Fates", "series": "Sword & Shield", "releaseDate": "2021/02/19"},
        "images": {"small": "https://images.pokemontcg.io/swsh45sv/SV107.png", "large": "https://images.pokemontcg.io/swsh45sv/SV107_hires.png"}
    },
    {
        "id": "sm9-14",
        "name": "Charizard & Braixen-GX",
        "set": {"id": "sm9", "name": "Team Up", "series": "Sun & Moon", "releaseDate": "2019/02/01"},
        "images": {"small": "https://images.pokemontcg.io/sm9/14.png", "large": "https://images.pokemontcg.io/sm9/14_hires.png"}
    },
    {
        "id": "sm115-9",
        "name": "Charizard-GX",
        "set": {"id": "sm115", "name": "Hidden Fates", "series": "Sun & Moon", "releaseDate": "2019/08/23"},
        "images": {"small": "https://images.pokemontcg.io/sm115/9.png", "large": "https://images.pokemontcg.io/sm115/9_hires.png"}
    },
    {
        "id": "sv3pt5-6",
        "name": "Charizard",
        "set": {"id": "sv3pt5", "name": "151", "series": "Scarlet & Violet", "releaseDate": "2023/09/22"},
        "images": {"small": "https://images.pokemontcg.io/sv3pt5/6.png", "large": "https://images.pokemontcg.io/sv3pt5/6_hires.png"}
    },
    {
        "id": "sv3-125",
        "name": "Charizard ex",
        "set": {"id": "sv3", "name": "Obsidian Flames", "series": "Scarlet & Violet", "releaseDate": "2023/08/11"},
        "images": {"small": "https://images.pokemontcg.io/sv3/125.png", "large": "https://images.pokemontcg.io/sv3/125_hires.png"}
    },
    {
        "id": "pgo-10",
        "name": "Charizard",
        "set": {"id": "pgo", "name": "Pokémon GO", "series": "Sword & Shield", "releaseDate": "2022/07/01"},
        "images": {"small": "https://images.pokemontcg.io/pgo/10.png", "large": "https://images.pokemontcg.io/pgo/10_hires.png"}
    },
    {
        "id": "det1-5",
        "name": "Charizard",
        "set": {"id": "det1", "name": "Detective Pikachu", "series": "Sun & Moon", "releaseDate": "2019/04/05"},
        "images": {"small": "https://images.pokemontcg.io/det1/5.png", "large": "https://images.pokemontcg.io/det1/5_hires.png"}
    },
    {
        "id": "swsh12pt5-25",
        "name": "Charizard",
        "set": {"id": "swsh12pt5", "name": "Crown Zenith", "series": "Sword & Shield", "releaseDate": "2023/01/20"},
        "images": {"small": "https://images.pokemontcg.io/swsh12pt5/25.png", "large": "https://images.pokemontcg.io/swsh12pt5/25_hires.png"}
    },
    {
        "id": "cel25-4",
        "name": "Charizard",
        "set": {"id": "cel25", "name": "Celebrations", "series": "Sword & Shield", "releaseDate": "2021/10/08"},
        "images": {"small": "https://images.pokemontcg.io/cel25/4.png", "large": "https://images.pokemontcg.io/cel25/4_hires.png"}
    },
    {
        "id": "neo4-6",
        "name": "Shining Charizard",
        "set": {"id": "neo4", "name": "Neo Destiny", "series": "Neo", "releaseDate": "2002/02/28"},
        "images": {"small": "https://images.pokemontcg.io/neo4/6.png", "large": "https://images.pokemontcg.io/neo4/6_hires.png"}
    },
    {
        "id": "base4-4",
        "name": "Charizard",
        "set": {"id": "base4", "name": "Base Set 2", "series": "Base", "releaseDate": "2000/02/24"},
        "images": {"small": "https://images.pokemontcg.io/base4/4.png", "large": "https://images.pokemontcg.io/base4/4_hires.png"}
    }
]

PRECACHED_DATA = {
    'pikachu': PIKACHU_CARDS,
    'meowscarada': MEOWSCARADA_CARDS,
    'mewtwo': MEWTWO_CARDS,
    'charizard': CHARIZARD_CARDS,
}

def get_precached_cards(query):

    if not query:
        return None

    normalized = query.strip().lower()

    if normalized in PRECACHED_DATA:
        return PRECACHED_DATA[normalized]

    for pokemon_name, cards in PRECACHED_DATA.items():
        if normalized.startswith(pokemon_name) or pokemon_name.startswith(normalized):
            if len(normalized) >= 2:
                return [c for c in cards if c['name'].lower().startswith(normalized)]

    return None

