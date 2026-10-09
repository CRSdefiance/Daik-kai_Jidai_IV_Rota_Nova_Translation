"""Translate B23's remaining crew and expedition messages and every clean native neighbor."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    2156: ("Leave it to me.", "Courteous assurance that the speaker will handle it."),
    2157: ("I'll give it my best!", "A cheerful promise to make an effort."),
    2158: ("This is exciting!", "The speaker feels excited with anticipation."),
    2159: ("It's my turn! I'll get it done!", "Rough voice says it is their turn and promises action."),
    2160: ("I'm raring to go!", "The speaker is full of enthusiasm and motivation."),
    2163: ("Whoa! What's going on?!", "Startled, polite question about what is happening."),
    2164: ("What's happening?!", "Agitated question about the situation."),
    2165: ("Whoa!!!", "A startled cry, without added facts."),
    2169: ("What? What? What?!", "Repeated startled questions."),
    2170: ("W-what's going on here...?", "Hesitant older formal voice asks what is happening."),
    2171: ("Ugh! I've been wounded!", "A pained recognition of suffering a wound."),
    2172: ("Urgh... I'm hurt...", "A strained recognition of injury."),
    2173: ("Ow! I'm bleeding...", "Pain and recognition of bleeding."),
    2174: ("Ow, ow...", "A repeated pained cry."),
    2175: ("Aw, I messed up...", "Rough, regretful admission of a mishap amid injury reports; no new cause or mechanism is invented."),
    2176: ("Ugh... I've been hurt...", "Recognition of injury after a pained cry."),
    2177: ("Oh no, I'm bleeding!", "Youthful distressed recognition of bleeding."),
    2182: ("%s's flagship was defeated! We've lost the battle!", "Confident informal voice reports the named flagship defeated and our defeat; no explicit sinking."),
    2183: ("%s's flagship's been beaten! We've lost the battle!", "Rough voice reports defeat of the named flagship and our side; does not assert sinking."),
    2185: ("%s's flagship was beaten! We've lost the battle!", "Youthful voice reports defeat of the named flagship and our side."),
    2186: ("%s's flagship has been defeated. We've lost!", "Formal older voice reports the named flagship defeated and our loss."),
    2187: ("We've defeated %s!", "Reports defeating the substituted target; does not invent its identity."),
    2193: ("...Hmm?", "A hesitant questioning reaction."),
    2194: ("Hm?", "A short questioning reaction."),
    2195: ("Ah!", "A sudden startled or noticing cry."),
    2196: ("...?", "A silent questioning pause, kept as its own native message."),
    2197: ("Hey! Stop slacking off!", "Calls out and orders someone to stop neglecting their duties."),
    2206: ("You're declaring war on me?! You must have a death wish! I'll send you to the bottom!", "Angrily calls declaring war suicidal and threatens to sink the challenger."),
    2207: ("What? What?! Please stop! Did I do something wrong?", "Frightened youthful voice asks for it to stop and wonders whether they did something wrong."),
    2234: ("They say the friendly local people will welcome us. Admiral, let's go!", "Hearsay that friendly indigenous inhabitants will welcome us; urges the admiral to go."),
    2235: ("I hear the kind local people will welcome us. Let's go!", "Informal hearsay about kind indigenous inhabitants welcoming us; urges departure."),
    2236: ("We're told the local people are friendly and will welcome us. Admiral, let's go!", "Formal hearsay about friendly indigenous inhabitants welcoming us; urges the admiral to go."),
    2237: ("It seems the friendly local people will welcome us. Admiral, shall we go right away?", "Older voice reports apparent welcome from friendly indigenous inhabitants and urges going promptly."),
    2240: ("The local people shared food and water with us!", "Informal report that indigenous inhabitants gave us food and water."),
    2241: ("The local people gave us some food and water!", "Older voice reports receiving food and water from indigenous inhabitants."),
    2242: ("The local people shared their food and water with us!", "Youthful report of indigenous inhabitants sharing food and water."),
    2243: ("Trouble! The local people attacked our expedition!", "Alarmed report that indigenous inhabitants attacked the expedition."),
    2249: ("The local people have attacked our expedition!", "Formal older report of indigenous inhabitants attacking the expedition."),
    2250: ("It looks like the expedition found nothing... Wait! Admiral, some sailors have deserted!", "Apparently no discoveries; sudden surprise reports that some sailors deserted."),
    2254: ("Apparently, the expedition found nothing. Prepare to leave... What?! Admiral, some sailors ran off!", "Reported lack of discoveries, order to prepare departure, then rough surprised report of deserting sailors."),
    2255: ("Apparently, the expedition found nothing. Prepare to leave... What?! Admiral, it seems some sailors have deserted!", "Older voice retains uncertainty about both no discoveries and prior desertion, plus departure preparations and surprise."),
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
            'context': (f'Independent native message {e.message_id}, COMMON B23 '
                        f'R{e.record_index}; readiness, injury, defeat, declarations, '
                        'local encounters or expedition results. Every native neighbor is included.'),
            'localization_note': ('Fresh clean-source English retains distinct crew reactions, '
                                  'injury versus bleeding, flagship defeat without invented '
                                  'sinking, angry versus frightened war responses, local '
                                  'indigenous inhabitants, kindness, food and water, attacks, '
                                  'uncertainty about discoveries and desertion, preparations '
                                  'to leave and surprise. Local people conveys the inhabitants '
                                  'naturally without adding an ethnicity. Silent questioning '
                                  'remains separate. Names and printf order are preserved. '
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
    Path('translations/common_japanese_b23_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
