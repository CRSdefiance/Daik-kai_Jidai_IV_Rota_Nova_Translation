"""Translate B22's remaining battle messages and every clean native neighbor."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    2031: ("I won't let so many of our comrades die for nothing. We have no choice... We surrender.", "Cannot let many comrades die in vain; surrender is unavoidable."),
    2032: ("It's hopeless... Admiral, this ship is surrendering...", "The situation is beyond saving; tells the admiral that this ship will surrender."),
    2041: ("You want to attack this town?! I won't let you!", "Confronts the attackers about their intention to attack the town and refuses to allow it."),
    2042: ("You're attacking this town?! Then don't expect any mercy!", "Roughly confronts the town's attackers and warns that they will receive no mercy."),
    2045: ("You've got some nerve attacking this town! We'll beat you back!", "Calls the intention to attack the town brazen and promises to defeat the attackers."),
    2046: ("The enemy flagship fled! We've won!", "The enemy flagship escaped; our side is victorious. Does not say the flagship sank."),
    2067: ("Enemy ship %s sunk!", "Brief report of sinking the named enemy ship."),
    2068: ("Admiral! We've sunk enemy ship %s!", "Excited report to the admiral that the named enemy ship has been sunk."),
    2069: ("We've sunk the enemy ship %s!", "Confident report of sinking the named enemy ship."),
    2070: ("We did it! Enemy ship %s sunk!", "Rough, triumphant celebration of sinking the named enemy ship."),
    2071: ("We've sunk the enemy ship %s!", "An older voice reports sinking the named enemy ship."),
    2099: ("Admiral, the enemy ship %s has raised a white flag! It looks like they're surrendering!", "Reports a raised white flag and apparent surrender by the named enemy ship, retaining uncertainty."),
    2100: ("Admiral, the enemy ship %s has surrendered!", "Informal report to the admiral of surrender by the named enemy ship."),
    2108: ("Our ram hit the enemy ship!", "Bright informal report that the ship's ram hit the enemy ship."),
    2109: ("Our ram struck the enemy ship!", "Confident report that the ship's ram hit the enemy ship."),
    2110: ("Our ram struck the enemy ship square in the side!", "Rough voice reports the ram striking the side of the enemy hull."),
    2111: ("Our ram's hit the enemy ship!", "Emphatic report that the ram hit the enemy ship."),
    2112: ("The ram hit the enemy ship!", "Youthful, excited report that the ram hit the enemy ship."),
    2113: ("Our ram has struck the enemy ship!", "Formal older voice reports the ram striking the enemy ship."),
    2114: ("Admiral, we're withdrawing!", "Formal report to the admiral of leaving the battle line."),
    2115: ("Admiral, we're disengaging!", "Concise formal report to the admiral of leaving the battle line."),
    2116: ("Admiral, we're pulling out!", "Informal report to the admiral of withdrawing from combat."),
    2117: ("Admiral, we're leaving the battle!", "Confident informal report to the admiral of withdrawing from combat."),
    2137: ("Admiral, victory belongs to us!", "Formal older voice reports our victory to the admiral."),
    2138: ("Our flagship has been defeated. We've lost!", "The flagship was defeated and our side lost; no explicit sinking claim."),
    2146: ("I'll show you the power of booze!", "Boastful older voice promises to demonstrate the power of alcohol."),
    2147: ("A battle, then!", "Polite voice acknowledges that a battle is beginning."),
    2148: ("So, it's a battle.", "A terse acknowledgment that this is a battle."),
    2149: ("A battle! I'll give it my best!", "Bright voice recognizes a battle and promises to try hard."),
    2150: ("A battle? This is my moment!", "Confident voice says that a battle is their opportunity to act."),
    2151: ("It's my turn now!", "Rough, emphatic declaration that it is the speaker's turn to act."),
    2152: ("A battle, eh!", "Older informal voice recognizes a battle."),
    2153: ("It's my turn, huh!", "Youthful voice acknowledges that it is their turn to act."),
    2154: ("A battle, I see!", "Formal older voice recognizes a battle."),
    2155: ("You can count on me!", "Asks the listener to expect good results from the speaker."),
}


def main():
    clean = NdsImage.open('work/clean.nds')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                     clean.read_file('/__arm9__.bin'))
    owners = {(entries[i].block, entries[i].record_index) for i in TEXT}
    selected = [e for e in entries if (e.block, e.record_index) in owners]
    assert {e.message_id for e in selected} == set(TEXT)
    rows = []
    for e in selected:
        english, meaning = TEXT[e.message_id]
        rows.append({
            'id': f'COMMON_MESSAGE_{e.message_id}', 'message_id': e.message_id,
            'block': e.block, 'record': e.record_index,
            'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
            'previous_japanese': entries[e.message_id - 1].text.decode('cp932'),
            'next_japanese': entries[e.message_id + 1].text.decode('cp932'),
            'english': english.replace('I', 'Ｉ').replace('F', 'Ｆ') + '{PAD}',
            'source_meaning': meaning,
            'speaker': 'Crew battle voice variant or town defender',
            'context': (f'Independent native message {e.message_id}, COMMON B22 '
                        f'R{e.record_index}; town defense, surrender, sinking, ram '
                        'impact, withdrawal or readiness. Every native neighbor is included.'),
            'localization_note': ('Fresh clean-source prose retains hopelessness, unavoidable '
                                  'surrender, refusal and no mercy, victory by flight rather '
                                  'than sinking, named enemy ships, the white flag and uncertain '
                                  'surrender, ram impact on the side, withdrawal, defeat and '
                                  'distinct boastful/polite/youthful voices. No gender is '
                                  'inferred for names or crew variants. Printf order is retained. '
                                  'Reserved I/F use existing narrow full-width glyphs. '
                                  'Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {
        'format': 'dk4-common-entry-manuscript-v1',
        'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
        'encoder': 'dialogue-fixed-v1',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'draft-awaiting-native-repack-and-formatting-review', 'records': rows,
    }
    Path('translations/common_japanese_b22_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
