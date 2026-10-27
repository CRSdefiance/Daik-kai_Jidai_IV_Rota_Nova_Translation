"""Author B20 crew/battle messages and all their native packed neighbors."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    1810: ("I'm feeling feverish...", "The speaker feels feverish; no diagnosis is asserted."),
    1811: ("An epidemic, huh... Well, some sleep should clear it up!", "The speaker calls the illness an epidemic but confidently expects sleep to cure it."),
    1824: ("I can't die yet...", "Defiant refusal to die yet."),
    1825: ("Has my time finally come...?", "An older voice wonders whether death has finally come to claim them."),
    1858: ("...I don't want to talk right now.", "The speaker does not want to speak at present."),
    1859: ("W-what happened???", "A hesitant, bewildered question about what happened."),
    1863: ("Raaagh!", "An inarticulate loud roar, without added factual meaning."),
    1864: ("What? What? What's happened?!", "An agitated older voice repeatedly asks what happened."),
    1871: ("@#$*!!", "Symbol-only angry outburst; actual profane words are not specified."),
    1872: ("Hey, don't get so angry. Come on.", "An informal attempt to calm someone who is angry."),
    1889: ("We're preparing for battle!", "Formal announcement that the crew is entering battle readiness."),
    1890: ("All hands to battle stations... Let's go!", "Orders everyone into battle readiness, followed by a forceful rally."),
    1891: ("We're getting ready for battle!", "Energetic informal announcement of battle readiness."),
    1892: ("We're preparing for battle! Let's get them!", "Confident announcement of battle readiness and an enthusiastic call to attack."),
    1897: ("We'll declare war on %s's faction. Is that correct?", "Formal confirmation of a declaration of war against the substituted party's faction."),
    1898: ("We're declaring war on %s's faction! Admiral, is that okay?", "Informal declaration against the substituted faction and confirmation addressed to the admiral."),
    1899: ("We'll declare war on %s's faction. Admiral, that's okay, right?", "Declaration against the substituted faction; the speaker seeks the admiral's assent."),
    1900: ("We're declaring war on %s's faction! You're sure, right?", "Rough, emphatic declaration and a direct request to confirm."),
    1901: ("We shall declare war on %s's faction. Do you agree?", "Authoritative declaration and formal confirmation."),
    1902: ("I'll tell %s's faction we're going to beat them! That's okay, right?", "A youthful voice describes the war declaration as telling the faction that we will beat them; asks for assent."),
    1903: ("We'll declare war on %s's faction. You approve, yes?", "Courteous, older-sounding confirmation of declaring war against the named faction."),
    1904: ("We don't know which faction this is, but we'll declare war. You're sure?", "Explicitly unknown faction identity; the speaker nevertheless confirms declaring war."),
    1905: ("We haven't identified this faction. Shall we declare war anyway?", "The faction has not been identified; formal confirmation of declaring war nonetheless."),
    1906: ("I don't know which faction this is. We're declaring war anyway, right?", "Informal uncertainty about faction identity and confirmation of declaring war."),
    1910: ("This faction is unidentified. Shall we declare war nonetheless?", "Formal older voice confirms declaring war even though the faction is unidentified."),
    1911: ("Admiral! It looks like %s's fleet will help us!", "Addressed to the admiral; the named fleet appears likely to reinforce us, retaining uncertainty."),
    1912: ("Admiral! %s's fleet will help us!", "Informal, confident report to the admiral that the named fleet will assist."),
    1913: ("Admiral! It looks like %s's fleet will join our side!", "Report to the admiral that the named fleet appears likely to reinforce our side."),
    1914: ("Admiral! It seems %s's fleet will help us out!", "Older informal voice reports apparent cooperation by the named fleet, retaining uncertainty."),
    1915: ("They say %s's fleet will fight alongside us too!", "Hearsay report that the named fleet will also fight together with us."),
}


def main():
    clean = NdsImage.open('work/clean.nds')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                     clean.read_file('/__arm9__.bin'))
    owners = {(entries[i].block, entries[i].record_index) for i in TEXT}
    selected = [e for e in entries if (e.block, e.record_index) in owners]
    assert {e.message_id for e in selected} == set(TEXT)
    rows = [{
        'id': f'COMMON_MESSAGE_{e.message_id}', 'message_id': e.message_id,
        'block': e.block, 'record': e.record_index,
        'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
        'previous_japanese': entries[e.message_id - 1].text.decode('cp932'),
        'next_japanese': entries[e.message_id + 1].text.decode('cp932'),
    } for e in selected]
    for row in rows:
        english, meaning = TEXT[row['message_id']]
        row.update(
            english=english.replace('I', 'Ｉ').replace('F', 'Ｆ') + '{PAD}',
            source_meaning=meaning,
            speaker='Crew voice variant or battle report narrator',
            context=(f"Independent native message {row['message_id']} in COMMON B20 "
                     f"R{row['record']}; illness, agitation, battle readiness, war "
                     "declaration or fleet assistance. All native neighbors are included."),
            localization_note=("Fresh clean-source English retains each voice, confirmation, "
                               "unknown faction, hearsay and apparent rather than certain aid. "
                               "Symbolic anger stays censored without invented profanity. "
                               "Printf argument order is unchanged. Reserved I/F use existing "
                               "narrow full-width glyphs. Native repack previews await review."),
            review={'source': True, 'context': True, 'localization': True,
                    'naturalness': True, 'formatting': False},
        )
    payload = {
        'format': 'dk4-common-entry-manuscript-v1',
        'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
        'encoder': 'dialogue-fixed-v1',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'draft-awaiting-native-repack-and-formatting-review', 'records': rows,
    }
    Path('translations/common_japanese_b20_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
