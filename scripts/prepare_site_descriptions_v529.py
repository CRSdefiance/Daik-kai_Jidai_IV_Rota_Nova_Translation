"""Clean-source, natural English descriptions for the 19 supported site images."""

import json
import textwrap
from pathlib import Path

ENGLISH = {
    0: 'A ring of standing stones near Salisbury in southern England, with a stone circle at its center. Explore from London to discover it and gain 5 influence.',
    2: 'A church in Hamburg, believed to be named for St. Martin, who lived in the 4th century. Discover it to gain 1 influence.',
    3: 'A wooden church in Stockholm, decorated with Christian and Norse motifs. Discover it to gain 1 influence.',
    5: "A cathedral in Seville, built in the 11th century. Its crypt honors James, one of Christ's twelve apostles. Discover it to gain 1 influence.",
    6: 'A vast oval arena begun by Emperor Vespasian in the 1st century. Explore from Genoa to discover it and gain 5 influence.',
    7: "A marble temple in Athens, built in the late 5th century BC. Its main chamber houses Athena, the city's patron goddess. Discover it to gain 3 influence.",
    8: 'Ruins of an underground city in central Anatolia, Turkey, thought to be about 1,000 years old. Explore from Istanbul to discover it and gain 5 influence.',
    9: 'The tombs of Khufu, Khafre, and Menkaure. The Sphinx is a creature from myth. Explore from Alexandria to discover them and gain 3 influence.',
    10: 'A grand mud-built mosque in Djenne, a thriving city south of the Sahara in West Africa. Explore from Sao Jorge to discover it and gain 10 influence.',
    11: "A vast stone building erected by the Rozwi in the 15th century. Zimbabwe means 'house of stone.' Explore from Sofala to discover it and gain 5 influence.",
    12: 'A royal mosque built by Shah Abbas I of the Safavid dynasty in the late 16th century. Explore from Basra to discover it and gain 15 influence.',
    13: 'A mausoleum built by Mughal emperor Shah Jahan for his queen, Mumtaz Mahal. Explore from Calicut to discover it and gain 15 influence.',
    14: 'A five-towered temple built in the 12th century by Suryavarman II of the ancient Khmer kingdom. Explore from Malacca to discover it and gain 20 influence.',
    15: 'Built in the late 8th century, its galleries on each level bear Buddhist reliefs. Explore from Batavia to discover it and gain 15 influence.',
    16: 'A Ming and Qing palace built by Emperor Yongle in the 15th century on the old Yuan palace site, after moving his capital from Nanjing. Explore from Hangzhou to discover it and gain 20 influence.',
    17: "The tomb of Muryeong, who ruled Baekje during its middle period. Its design reflects tombs of China's Southern Dynasties. It stands in the hills of the former capital, Ungjin. Explore from Seoul to discover it and gain 20 influence.",
    18: "An ornate gold-leaf pavilion built in Kyoto's Kitayama in the 14th century by the third Muromachi shogun. Explore from Osaka to discover it and gain 20 influence.",
    19: "Stone warrior statues at the ruins of Tula, capital of Mexico's ancient Toltec kingdom. Explore from Havana to discover them and gain 15 influence.",
    20: 'Pyramids left by Teotihuacan, said to have been built around the 2nd century AD. Explore from Veracruz to discover them and gain 15 influence.',
}

FACTS = {
    0: 'Salisbury in southern England; a megalithic ring with a stone circle at its center; exploration from London; influence +5.',
    2: 'Hamburg church, believed named for the fourth-century saint Martinus; discovery gives influence +1.',
    3: 'Stockholm wooden church; Christian and Norse mythology motifs; discovery gives influence +1.',
    5: 'Seville cathedral built in the eleventh century; underground sanctuary honors James, one of the twelve apostles; discovery gives influence +1.',
    6: 'Large-capacity oval arena begun by Roman emperor Vespasian in the first century; exploration from Genoa; influence +5.',
    7: 'Athens marble temple built in the latter fifth century BC; main chamber houses patron goddess Athena; discovery gives influence +3.',
    8: 'Underground city ruins in central Anatolia, Turkey, estimated one thousand years old; exploration from Istanbul; influence +5.',
    9: 'Tombs of Khufu, Khafre and Menkaure; Sphinx is a mythical monster; exploration from Alexandria; influence +3.',
    10: 'Grand mosque made of mud at Djenne, which flourished south of the Sahara in West Africa; exploration from Sao Jorge; influence +10.',
    11: 'Huge stone building; source attributes construction to Rozwi in the fifteenth century; Zimbabwe means house of stone; exploration from Sofala; influence +5.',
    12: 'Royal mosque attributed to Safavid Shah Abbas I in the late sixteenth century; exploration from Basra; influence +15.',
    13: 'Mughal emperor Shah Jahan built a mausoleum for Queen Mumtaz Mahal; exploration from Calicut; influence +15.',
    14: 'Five-spired temple built in the twelfth century by Suryavarman II of the ancient Khmer kingdom; exploration from Malacca; influence +20.',
    15: 'Built in the late eighth century; Buddhist reliefs in galleries on each level; exploration from Batavia; influence +15.',
    16: 'Ming and Qing imperial palace; Yongle built it in the fifteenth century on the former Yuan palace site after moving the capital from Nanjing; exploration from Hangzhou; influence +20.',
    17: 'Mid-period Baekje king Muryeong tomb, influenced by Chinese Southern Dynasties burial practices; hills at then-capital Ungjin; exploration from Seoul; influence +20.',
    18: 'Lavish gold-leaf pavilion at Kyoto Kitayama, built in the fourteenth century by the third Muromachi shogun; exploration from Osaka; influence +20.',
    19: 'Stone warrior statues at Tula, capital of ancient Mexico Toltec kingdom; exploration from Havana; influence +15.',
    20: 'Teotihuacan pyramids, said to date to around the second century AD; exploration from Veracruz; influence +15.',
}


def main():
    source = json.loads(Path('work/analysis/site_descriptions_v529/source_inventory.json').read_text(encoding='utf-8'))
    rows = []
    for row in source['source_rows']:
        index = row['site_id']
        if not row['image_owner_pointer']:
            assert index in (1, 4) and row['japanese'] == '無い無い'
            continue
        english = ENGLISH[index]
        assert '\n' not in english and not english.startswith(' ')
        lines = textwrap.wrap(english, 42, break_long_words=False, break_on_hyphens=False)
        assert len(lines) <= 11 and ' '.join(lines) == english
        rows.append({**row, 'id': f'HISTORIC_SITE_DESCRIPTION_{index:02d}',
                     'english': english, 'speaker': 'Gallery narrator',
                     'context': 'Original Historic Sites image viewer; selected site caption above a static explanatory paragraph. Adjacent entries are separate sites, not dialogue.',
                     'source_meaning': FACTS[index],
                     'localization_note': 'Preserve the source account, dates, attribution, discovery port and exact influence reward. Use established English proper names and natural sentences. Do not silently revise historical claims or add story facts. Paragraph wraps are generated by the static Gallery formatter, without authored indentation.',
                     'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False},
                     'formatting_review_pending': True, 'preview_lines': lines})
    document = {'format': 'dk4-historic-site-description-manuscript-v1',
                'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                'source_inventory': 'work/analysis/site_descriptions_v529/source_inventory.json',
                'records': rows, 'unsupported_source_entries_preserved': [1, 4],
                'authored_line_breaks_or_indent_spaces': False,
                'native_pixel_and_allocation_review_pending': True}
    Path('translations/historic_site_description_manuscript_v1.json').write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('19 complete source-reviewed paragraphs:', sum(len(r['english']) + 1 for r in rows),
          'bytes before compiled formatting; original capacity', sum(r['source_aligned_capacity'] for r in rows))


if __name__ == '__main__':
    main()
