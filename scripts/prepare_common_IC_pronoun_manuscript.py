"""Repair every COMMON IC pronoun occurrence and its clean native neighbors."""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    527: ("Listen to the admiral! If you won't obey, you'll have to face me!", "Orders obedience to the admiral and threatens personal opposition if the listener disobeys."),
    566: ("Got it! Leave the rest to me!", "Acknowledges the order and offers to handle what remains."),
    792: ("Admiral, I'll help repair it too!", "Offers the speaker's help with repairs in addition to others."),
    793: ("Admiral, let me help repair it too.", "Asks permission to help with repairs as well."),
    1118: ("Then I'll draft the diplomatic letter. What should it say?", "Offers to write the letter for negotiations and asks what its contents should be."),
    1140: ("I can't imagine %s coming under our command... Are you really going ahead with this?", "Doubts that the named party would submit to our authority; asks whether to really proceed."),
    1257: ("Admiral, I'll help remodel it too!", "Offers to help with ship remodeling in addition to others."),
    1477: ("I'll handle the diplomatic talks!", "Offers to handle diplomatic negotiations."),
    1561: ("It's our ship, so we have to keep it clean!", "The ship belongs to us, so we must clean it."),
    1610: ("I'm here, so don't worry!", "Reassures the listener because the speaker is present."),
    1747: ("I'll lead the boarding fight!", "The speaker will take the lead in close-quarters boarding combat."),
    1783: ("I'm exhausted... Let me rest...", "The speaker is worn out and asks to rest."),
    2131: ("Admiral, victory is ours!", "Formal report of victory for our side addressed to the admiral."),
    2132: ("Admiral, we've won!", "Enthusiastic report to the admiral of our victory."),
    2178: ("...I've been wounded.", "The speaker has suffered a wound."),
    2179: ("%s's flagship has been defeated. We've lost!", "The named party's flagship was defeated; our side has lost. Does not assert sinking."),
    2180: ("%s's flagship was sunk! We've lost!", "The named party's flagship was explicitly sunk; our side lost."),
    2181: ("%s's flagship was defeated! We've lost the battle!", "Informal report that the named flagship was defeated and our side lost; no sinking claim."),
    2295: ("I never expected an oasis here. What a relief...", "Finding an oasis in such a place was unexpected and welcome."),
    2296: ("An oasis here? We must be lucky!", "The unexpected oasis makes the speaker conclude that we are lucky."),
    2501: ("Admiral, if you take that away, I won't be able to do my job.", "Removing the indicated item would prevent the speaker from doing their job; no item or role is invented."),
    2543: ("We've defeated the %s / %s fleet! We've won!", "Defeated the fleet with the paired substituted identifier; our side won. Both substitutions remain ordered."),
    2554: ("The %s / %s fleet has defeated us...", "Our side was defeated by the fleet identified by the two ordered substituted labels."),
    2560: ("The %s / %s fleet was tougher than we expected. Our fleet has retreated...", "The opposing fleet was stronger than expected and our fleet withdrew; both facts and argument order remain."),
    2640: ("We've won!", "Informal report of victory for our side."),
    2641: ("Victory is ours!", "Formal report of victory for our side."),
    2645: ("Our fleet has been defeated...", "Formal report that our fleet was defeated."),
    2646: ("Our fleet's been defeated...", "Informal report that our fleet was defeated."),
    2652: ("Our fleet has retreated...", "Report that our fleet withdrew, without adding a claim of destruction."),
}


def main():
    clean = NdsImage.open('work/clean.nds')
    arm9 = clean.read_file('/__arm9__.bin')
    for lo, hi, digest in (
        (0x53914, 0x53AC4, '71f0a5626d1992a8e2a2f0fb5a287bb42d719c0861488c64aec7ea5fe5386d87'),
        (0x7E9B8, 0x7E9D0, '3aa4bb7ba550c0e7daab45dd6d3912ebd38c99facaad78be015a422736ccd76b'),
    ):
        assert hashlib.sha256(arm9[lo:hi]).hexdigest() == digest
    assert arm9[0x143A28:0x143A2B] == bytes.fromhex('966C00')
    assert arm9[0x143A2C:0x143A33] == bytes.fromhex('8341835E835600')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), arm9)
    owners = {(e.block, e.record_index) for e in entries if b'IC' in e.text}
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
            'speaker': 'Crew voice variant or battle report narrator',
            'context': (f'Independent native message {e.message_id}, COMMON '
                        f'B{e.block} R{e.record_index}. Source-locked ARM9 IC mapping '
                        'proves first-person pronouns; all packed neighbors are included.'),
            'localization_note': ('IC expands to 僕 or アタシ in the unchanged ARM9 parser, '
                                  'so natural English uses I or we/us/our with a plural suffix. '
                                  'No gender, name or rank is inferred. Older mismatched selections '
                                  'are replaced from clean Japanese, retaining ship cleaning, '
                                  'diplomatic contents, authority, equipment conditions, nearby '
                                  'oasis, defeat versus sinking and retreat. Paired fleet labels '
                                  'stay in source order with a neutral slash, without inventing '
                                  'two separate fleets or a hierarchy. Those actual values need '
                                  'runtime review. Reserved I/F use narrow full-width glyphs; '
                                  'exact-font preview review remains pending.'),
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
    Path('translations/common_IC_pronoun_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
