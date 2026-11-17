from collections.abc import Iterator

PathwayRow = tuple[str, str, str, str]

CHURCH_OF_ETERNAL_NIGHT = "Церковь Вечной Ночи"
CHURCH_OF_STORMS = "Церковь Повелителя Бури"
CHURCH_OF_STEAM_AND_MACHINERY = "Церковь Бога Пара и Машин"

_PATHWAYS: tuple[
    tuple[str, str, tuple[tuple[str, str], ...]],
    ...,
] = (
    (
        "Darkness",
        CHURCH_OF_ETERNAL_NIGHT,
        (
            ("Неспящий", "Sleepless"),
            ("Полуночный поэт", "Midnight Poet"),
            ("Кошмар", "Nightmare"),
            ("Хранитель душ", "Soul Assurer"),
            ("Чернокнижник духов", "Spirit Warlock"),
            ("Ночной страж", "Nightwatcher"),
            ("Епископ ужаса", "Horror Bishop"),
            ("Слуга сокрытия", "Servant of Concealment"),
            ("Рыцарь несчастья", "Knight of Misfortune"),
            ("Тьма", "Darkness"),
        ),
    ),
    (
        "Death",
        CHURCH_OF_ETERNAL_NIGHT,
        (
            ("Собиратель трупов", "Corpse Collector"),
            ("Могильщик", "Gravedigger"),
            ("Медиум", "Spirit Medium"),
            ("Проводник духов", "Spirit Guide"),
            ("Привратник", "Gatekeeper"),
            ("Бессмертный", "Undying"),
            ("Перевозчик", "Ferryman"),
            ("Консул смерти", "Death Consul"),
            ("Бледный император", "Pale Emperor"),
            ("Смерть", "Death"),
        ),
    ),
    (
        "Tyrant",
        CHURCH_OF_STORMS,
        (
            ("Моряк", "Sailor"),
            ("Народ гнева", "Folk of Rage"),
            ("Мореход", "Seafarer"),
            ("Благословлённый ветром", "Wind-blessed"),
            ("Песнопевец океана", "Ocean Songster"),
            ("Вершитель катастроф", "Cataclysmic Interrer"),
            ("Морской король", "Sea King"),
            ("Бедствие", "Calamity"),
            ("Бог грома", "Thunder God"),
            ("Тиран", "Tyrant"),
        ),
    ),
    (
        "White Tower",
        CHURCH_OF_STORMS,
        (
            ("Читатель", "Reader"),
            ("Ученик логики", "Student of Ratiocination"),
            ("Детектив", "Detective"),
            ("Эрудит", "Polymath"),
            ("Магистр мистицизма", "Mysticism Magister"),
            ("Пророк", "Prophet"),
            ("Познающий", "Cognizer"),
            ("Ангел мудрости", "Wisdom Angel"),
            ("Всевидящее око", "Omniscient Eye"),
            ("Белая Башня", "White Tower"),
        ),
    ),
    (
        "Paragon",
        CHURCH_OF_STEAM_AND_MACHINERY,
        (
            ("Учёный", "Savant"),
            ("Археолог", "Archaeologist"),
            ("Оценщик", "Appraiser"),
            ("Ремесленник", "Artisan"),
            ("Астроном", "Astronomer"),
            ("Алхимик", "Alchemist"),
            ("Тайный учёный", "Arcane Scholar"),
            ("Магистр знаний", "Knowledge Magister"),
            ("Просветитель", "Illuminator"),
            ("Парагон", "Paragon"),
        ),
    ),
    (
        "Hermit",
        CHURCH_OF_STEAM_AND_MACHINERY,
        (
            ("Искатель тайн", "Mystery Pryer"),
            ("Учёный-рукопашник", "Melee Scholar"),
            ("Колдун", "Warlock"),
            ("Профессор свитков", "Scrolls Professor"),
            ("Мастер созвездий", "Constellations Master"),
            ("Мистиколог", "Mysticologist"),
            ("Ясновидец", "Clairvoyant"),
            ("Мудрец", "Sage"),
            ("Император знаний", "Knowledge Emperor"),
            ("Отшельник", "Hermit"),
        ),
    ),
)


def pathway_rows() -> Iterator[PathwayRow]:
    for pathway_name, church, sequences in _PATHWAYS:
        for sequence_number, (russian_name, english_name) in enumerate(sequences[::-1]):
            yield (
                f"{sequence_number}{pathway_name}",
                russian_name,
                english_name,
                church,
            )
