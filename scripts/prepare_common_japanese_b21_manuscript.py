"""Translate B21's remaining battle messages from verified clean native spans."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    1921: ("It looks like %s's nearby fleet will help us too!", "The nearby named fleet apparently will also assist; retains uncertainty and 'also'."),
    1922: ("I hear %s's nearby fleet will lend us a hand!", "Hearsay that the nearby named fleet will assist."),
    1923: ("It seems %s's nearby fleet will join our side too!", "Formal older voice reports apparent assistance by the nearby named fleet, also joining us."),
    1924: ("Admiral, we've shot the enemy admiral! Victory is ours!", "The enemy admiral was shot by a marksman; victory follows. Does not add a claim of death."),
    1932: ("You're %s! Face me in a fair duel!", "Recognizes the opponent and demands a fair, honorable single combat."),
    1933: ("Ah, you're %s! Let's duel!", "Surprised recognition and a challenge to single combat."),
    1934: ("So, you're %s! Let's settle this with a duel!", "Confident recognition and challenge to decide the matter in single combat."),
    1935: ("Hey, %s! Fight me one on one!", "Rough recognition and forceful demand for one-on-one combat."),
    1938: ("...You're %s! We shall settle this with a duel!", "Authoritative recognition followed by a demand to settle the matter in single combat."),
    1939: ("Interesting! I accept your challenge!", "Formal acceptance; the challenge interests the speaker."),
    1941: ("All right! I'll take you on!", "Bright, informal acceptance of the challenge."),
    1942: ("Bring it on! I accept your challenge!", "Confident, emphatic acceptance of the challenge."),
    1943: ("This'll be fun! I'll take you on!", "Rough, enthusiastic voice finds the challenge interesting and accepts."),
    1944: ("All right! Let's do this!", "Emphatic agreement to undertake the fight."),
    1945: ("Next time won't be so easy!", "Warns that the next encounter will not go the same way."),
    1946: ("You won't get away next time!", "Confident warning that the opponent will not escape next time."),
    1947: ("You're not getting away next time!", "Rough, emphatic warning that the opponent will not escape next time."),
    1951: ("%s, please get away! Everyone, give them cover!", "Asks the named person to escape and orders everyone to provide covering support."),
    1952: ("%s, hurry and get away! We'll all give you cover!", "Urges the named person to escape quickly; everyone will provide covering support."),
    1953: ("%s, get away now! Everyone, give them cover!", "Urges the named person to escape quickly and rallies everyone to provide cover."),
    1954: ("%s, get out of here! Come on, lads, cover them!", "Rough call to the named person to escape; rallies the men to provide covering support."),
    1957: ("Perfect!", "A brief cry that the action was just right."),
    1958: ("...I've read your move!", "The speaker has seen through the opponent's move."),
    1959: ("That attack won't work on me!", "Dismisses the effectiveness of the opponent's attack."),
    1962: ("There! One strike, right on target!", "An older voice exults in a strike that hits its mark."),
    1963: ("Yay! I hit you!", "A youthful voice joyfully celebrates landing a hit."),
    1964: ("Good! Right here!", "The speaker identifies the precise spot or opening in battle."),
    1969: ("Tch! I rushed that a little!", "Rough voice admits to getting impatient or acting too hastily."),
    1970: ("Ugh... No matter. This fight is just getting started!", "An older voice reacts to a setback but insists the fight is only beginning."),
    1985: ("That swordplay is child's play compared to Gerhard's training!", "Dismisses the enemy's swordsmanship by comparison with Gerhard's demanding training; no new family/title claim."),
    1986: ("Think brute-force swings will work on me? Take this!", "Dismisses sword attacks relying only on strength, then launches a counterattack."),
    1987: ("Ha ha ha! It's showtime!", "Boisterous laughter and announcement that the show is beginning."),
    1988: ("Hey, hey! What's the matter? I'm not even trying yet!", "Taunts the opponent and says the speaker has not yet begun fighting seriously."),
    1989: ("I'll show you swordplay honed on the battlefield!", "Promises to demonstrate swordsmanship developed in real battle."),
    1995: ("Admiral! %s has surrendered!", "Excited report to the admiral that the named party has surrendered."),
    1996: ("%s has given up!", "Rough, deferential report of surrender by the named party."),
    2005: ("We've destroyed the enemy flagship!", "Formal older voice reports destruction of the enemy flagship, without adding its method."),
    2006: ("Admiral, our flagship's been hit! We can't stop the flooding!", "Our flagship has been struck or defeated; water ingress can no longer be stopped."),
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
            'speaker': 'Crew battle voice variant or battle report narrator',
            'context': (f'Independent native message {e.message_id}, COMMON B21 '
                        f'R{e.record_index}; fleet aid, duels, escape cover, combat '
                        'taunts, surrender or flagship damage. Every packed neighbor is included.'),
            'localization_note': ('Fresh clean-source English preserves nearby/also/uncertainty '
                                  'and hearsay in aid reports, honor in the duel challenge, '
                                  'single combat, urgency, covering support, distinct voices, '
                                  'Gerhard and both flagship damage and unstoppable flooding. '
                                  'No gender or death is inferred from substituted names. '
                                  'Printf order is preserved; reserved I/F use narrow full-width '
                                  'glyphs. Exact-font preview review remains pending.'),
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
    Path('translations/common_japanese_b21_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
