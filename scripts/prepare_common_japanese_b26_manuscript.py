"""Prepare clean-source small-shark decisions, sea events and item-use reports."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    2430: ('Admiral, what should we do with it?', 'Asks the admiral what to do with the captured small shark.'),
    2431: ('Sharks may be monsters, but I feel bad about killing one this small...', 'Reluctant to kill such a small shark despite sharks being regarded as monsters.'),
    2432: ("Even if it's a shark, I feel bad about killing something so small.", 'Hesitates to kill the creature because it is so small, even though it is a shark.'),
    2435: ("Release it into the sea?! You've got to be kidding! Just think what might happen when it's fully grown!", 'Rough alarm and objection to releasing the shark into the sea; urges considering what happens when it grows.'),
    2436: ('What?! Are you serious?', 'Surprised question whether the preceding decision is serious.'),
    2437: ("Yes. I'm looking forward to seeing what happens.", 'Affirms the decision and looks forward to its outcome.'),
    2438: ("Yes. I'm serious.", 'Firmly affirms the preceding decision is serious.'),
    2439: ("Yes, though I don't know what will happen...", 'Affirms the decision while admitting uncertainty about the outcome.'),
    2443: ('Hey, can I say something?', 'Casual request to speak or interrupt.'),
    2444: ("What's wrong?", 'Asks what is the matter.'),
    2445: ('What is it?', 'Directly asks what is the matter.'),
    2446: ('What?', 'Blunt feminine question in response to the request to speak.'),
    2447: ('Yes? What is it?', 'Gentler feminine question in response to the request to speak.'),
    2452: ("That's the spirit! Oh, I can't wait! I'm so excited!", 'Enthusiastic approval and excited anticipation of the shark-food decision.'),
    2456: ("Ah! The wind's starting to blow!", 'Notices that the wind has begun blowing.'),
    2457: ('Oh, it seems the wind has started blowing. What a relief!', 'Feminine voice reports an apparent return of wind and relief.'),
    2458: ("Oh! The wind's starting to blow!", 'Rough pleased report that wind has begun blowing.'),
    2459: ('Oh! It seems the wind has risen!', 'Older pleased report of wind apparently beginning to blow.'),
    2460: ("Wind! Hooray, the wind's blowing!", 'Youthful delight at the wind beginning to blow.'),
    2461: ('The wind has started blowing.', 'Formal older observation that wind has begun blowing.'),
    2462: ('Perhaps it had to fight because foolish humans decided to treat it like a monster...', "Speculates that foolish humans' arbitrary treatment of the creature as a monster forced it to fight."),
    2464: ('Maybe I should feel sorry for it...', 'Wonders whether the creature is actually pitiful.'),
    2465: ('Perhaps it has to fight because humans treated it as a monster. Maybe we should feel sorry for this animal...', 'Feminine speculation that arbitrary treatment by humans left it no choice but to fight, and perhaps it deserves pity.'),
    2468: ('Maybe it has to fight because people call it a monster? I feel sorry for it...', 'Youthful question whether being called a monster forced it to fight; feels pity.'),
    2469: ("Admiral, look over there! Something's shining!", "Calls the admiral's attention to something shining over there."),
    2488: ('The ram smashed the floating ice!', 'Rough report that the ram smashed drift ice.'),
    2489: ("The ram destroyed the floating ice! We needn't worry about the ship being damaged!", 'Older report of drift ice destroyed by the ram and reassurance about ship damage.'),
    2490: ('The ram shattered the floating ice!', 'Youthful report that the ram broke apart drift ice.'),
    2491: ('Admiral, thanks to the ram smashing the floating ice, the ship suffered no damage!', 'Formal older report to the admiral that the ram broke drift ice and thus no damage occurred.'),
    2498: ('Hooray, a feast tonight!', 'Youthful excitement at a feast tonight following the treasure discovery.'),
    2499: ("What magnificent treasure... I never expected this! It's all thanks to you, Admiral.", "Formal older amazement at the treasure's greatness and credits the admiral for it all."),
    2505: ("We don't seem to need it right now.", 'Apparently no current need to use the item.'),
    2506: ("We don't need to use it now, do we?", 'Informal question suggesting the item need not be used now.'),
    2507: ("We don't seem to need to use it yet.", 'Older tentative judgment that the item need not be used now.'),
    2510: ('We gave %s to the sailors.', 'Reports giving the substituted item to the sailors.'),
    2511: ('We gave %s to the sailors.', 'Informal report of giving the substituted item to the sailors.'),
    2512: ('No one knows how to use it.', 'States that no one knows how to use the item.'),
    2513: ('How do you use it? It seems nobody knows the answer.', 'Asks how the item is used and says apparently no one knows.'),
    2514: ("What's that? It seems no one knows how to use it.", 'Older question what the item is and tentative report that no one knows its use.'),
    2515: ('How do you use it? It looks like no one knows.', 'Feminine question how to use the item and tentative report of universal ignorance.'),
    2521: ('The cat got rid of the rats.', 'Informal report that the cat eliminated the rats.'),
    2522: ('We had the cat get rid of the rats.', 'Older report that the cat was made to eliminate the rats.'),
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
            'speaker': 'Crew sea-event voice variant or protagonist granting log permission',
            'context': (f'Independent native message {e.message_id}, clean COMMON B26 '
                        f'R{e.record_index}; small-shark choices, wind, ice, treasure and item-use events. '
                        'All native selections in each selected source owner are included.'),
            'localization_note': ('Fresh clean-source American English preserves disagreement about killing '
                                  'or releasing a small shark, future danger, uncertainty and anticipation, '
                                  'returning wind, speculation that humans forced the creature to fight, pity, '
                                  'floating ice and ram protection, the feast tonight, credit to the admiral, '
                                  'tentative item-use decisions, sailor gifts and cat pest control. No invented '
                                  'outcomes or relationships. Printf argument shape and order are preserved. '
                                  'One paragraph; safe full-width I/F. Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-reblocking-and-formatting-review', 'records': rows}
    Path('translations/common_japanese_b26_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(rows)} clean-source native messages')


if __name__ == '__main__':
    main()
