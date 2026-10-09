"""Author all BGM titles from clean Japanese, independently of old allocations."""
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

# Source, localization, faithful gloss. The musical titles do not imply a
# named speaker or additional story facts. Keep the original regional scope.
TITLES = (
    ('勇躍', 'In High Spirits', 'Eager, spirited enthusiasm.'),
    ('エンディング', 'Ending', 'The ending.'),
    ('追い風に乗って', 'Riding the Tailwind', 'Riding with a following wind.'),
    ('旅立ちのテーマ', 'Departure Theme', 'Theme of setting out on a journey.'),
    ('南へ行こう', "Let's Head South", 'An invitation to go south.'),
    ('インディアの風', 'Winds of India', 'The wind of India.'),
    ('南海の島々', 'South Sea Islands', 'The islands of the southern seas.'),
    ('東アジアの海', 'Seas of East Asia', 'The sea of East Asia.'),
    ('水平線の向こうへ', 'Beyond the Horizon', 'Toward the other side of the horizon.'),
    ('北欧の街', 'North European Town', 'A town in northern Europe.'),
    ('南欧の街', 'South European Town', 'A town in southern Europe.'),
    ('イスラムの町', 'Islamic Town', 'A town of the Islamic world.'),
    ('アフリカの町', 'African Town', 'A town in Africa.'),
    ('インドの町', 'Indian Town', 'A town in India.'),
    ('東南アジアの集落', 'Southeast Asian Village', 'A settlement or village in Southeast Asia.'),
    ('中国の町', 'Chinese Town', 'A town in China.'),
    ('日本の町', 'Japanese Town', 'A town in Japan.'),
    ('新大陸の町', 'New World Town', 'A town in the New World.'),
    ('洋上戦闘のテーマ', 'Naval Battle Theme', 'Theme for combat at sea.'),
    ('大海戦', 'Great Naval Battle', 'A great or large-scale battle at sea.'),
    ('海へ続く道', 'The Road to the Sea', 'A road leading to the sea.'),
    ('本当の宝物', 'The True Treasure', 'The true treasure, not specifically a gemstone.'),
    ('波', 'Waves', 'Waves; Japanese does not mark singular versus plural.'),
    ('情熱の炎', 'Flames of Passion', 'The flame of passion.'),
    ('ラファエル', 'Raphael', 'The character Raphael.'),
    ('ホドラム', 'Hodram', 'The character Hodram.'),
    ('リルとカミル', 'Lil & Kamil', 'Lil and Kamil together.'),
    ('探検！探検！', 'Explore! Explore!', 'An enthusiastic, deliberately repeated call to explore.'),
    ('暗雲', 'Dark Clouds', 'Dark clouds, including the sense of looming trouble.'),
    ('麗しの乙女', 'Fair Maiden', 'A beautiful maiden.'),
    ('想い', 'Feelings', 'Thoughts or heartfelt feelings; the title leaves their object unspecified.'),
    ('陽気な仲間', 'Merry Companions', 'Cheerful companions.'),
    ('悲しみ', 'Sorrow', 'Sadness or sorrow.'),
    ('海賊王', 'The Pirate King', 'The pirate king; the king element is essential.'),
    ('征服者', 'The Conqueror', 'A conqueror, rather than merely a victor.'),
    ('強敵登場', 'A Mighty Foe Appears', 'The arrival of a powerful opponent.'),
    ('大勝利！', 'Great Victory!', 'An emphatic great victory.'),
    ('オープニング', 'Opening', 'The opening.'),
)


def main():
    clean = NdsImage.open('work/clean.nds')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                     clean.read_file('/__arm9__.bin'))
    assert len(TITLES) == 38
    rows = []
    for i, (japanese, english, meaning) in enumerate(TITLES, 3251):
        entry = entries[i]
        if entry.text.decode('cp932') != japanese:
            raise ValueError(f'Clean BGM source differs at {i}')
        english.encode('ascii')
        rows.append({
            'id': f'COMMON_MESSAGE_{i}', 'message_id': i,
            'block': entry.block, 'record': entry.record_index,
            'source_hex': entry.text.hex().upper(), 'japanese': japanese,
            'previous_japanese': entries[i - 1].text.decode('cp932'),
            'next_japanese': entries[i + 1].text.decode('cp932'),
            'english': english + '{PAD}', 'source_meaning': meaning,
            'speaker': 'Sound Setup BGM title label',
            'context': (f'Native global message {i}, clean B{entry.block} '
                        f'R{entry.record_index}; BGM selector title, displayed by '
                        'the independent ASCII title renderer at ARM9 0x1091FC. '
                        'Messages 3286-3288 share an owner with promotional '
                        'messages 3289-3290, whose presentation is still unclassified.'),
            'localization_note': ('Fresh source review restores the whole title meaning, '
                                  'including regions, settlement type, theme, repetition, '
                                  'treasure, king, conqueror and powerful opponent. '
                                  'Established character spellings are retained. '
                                  'Plain ASCII is required by this title renderer; '
                                  'shared-dialogue full-width I/F replacements do not apply. '
                                  'No manual wrapping or abbreviation to mimic old allocations. '
                                  'Panel and packed-owner integration remain pending.'),
            'presentation': 'sound-bgm-title-ascii',
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {
        'format': 'dk4-common-entry-manuscript-v1',
        'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
        'encoder': 'dialogue-fixed-v1',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'draft-awaiting-title-renderer-and-complete-owner-integration',
        'records': rows,
    }
    destination = Path('translations/common_bgm_complete_titles_v2.json')
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n',
                           encoding='utf-8')
    print(f'Prepared {len(rows)} full clean-source BGM titles: {destination}')


if __name__ == '__main__':
    main()
