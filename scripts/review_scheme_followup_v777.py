"""Pin clean sources and review scheme follow-ups, bribery and one separate rumor."""

import re
from dataclasses import asdict
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/scheme_followup_editorial_v777')
CURRENT = Path('out/all_routes_combined_v776_candidate.nds')
MANUSCRIPT = Path('translations/scheme_followup_editorial_manuscript_v1.json')
TABLES = {
    0x02118240: (964, 965, 966, 967, 968, 969, 970, 971),
    0x02118220: (973, -1, 974, -1, 975, 976, 977, -1),
    0x02118200: (978, 979, 980, -1, 981, 982, 983, -1),
    0x021181E0: (984, -1, 985, -1, 986, 987, 988, -1),
}
TEXTS = {
    964: "I'll make the arrangements. I'm looking forward to seeing how it turns out.",
    965: "I'll make the arrangements. Let's wait for good news.",
    966: "Leave the arrangements to me. I wonder how it'll turn out...",
    967: "Leave the rest to me. I hope it goes well.",
    968: "Leave the arrangements to me. I'm looking forward to seeing how it turns out...",
    969: "I'll see to the arrangements. I'm eager to see what happens...",
    970: "I'll handle the rest. I wonder if it'll work out...",
    971: "I'll make the arrangements. I'm looking forward to the results.",
    972: "The ship due on this month's regular run apparently sank in a storm...",
    973: "Which town's broker shall we bribe?",
    974: "Which town's broker do you plan to bribe?",
    975: "Which town's broker are we bribing?",
    976: "Which town's broker shall we bribe?",
    977: "Which town's broker should we bribe?",
    978: "In %s, we're to bribe %s's broker, correct?",
    979: "In %s, we're to bribe %s's broker. Is that correct?",
    980: "So, in %s, we're bribing %s's broker, right?",
    981: "In %s, I should bribe %s's broker. Is that right?",
    982: "In %s, we're to bribe %s's broker, then?",
    983: "In %s, we're bribing %s's broker, right?",
    984: "Admiral, it's packed. There's nowhere to sit and talk privately. Let's try another day.",
    985: "With this crowd, we can't talk privately. Let's try another day.",
    986: "Admiral, with this crowd, we can't talk privately. Let's come back another day.",
    987: "There isn't a seat where we can talk privately. Shall we come back later, Admiral?",
    988: "Wow, it's so crowded! We can't talk privately here. Let's try tomorrow.",
}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    paths = [Path('work/clean.nds'), Path('out/raphael_natural_v2_accepted_base.nds'), CURRENT]
    roms = [NdsImage.open(p) for p in paths]
    arms = [r.read_file('/__arm9__.bin') for r in roms]
    commons = [r.read_file('/COMMON/MESFILE.DK4') for r in roms]
    entries = [common_message_entries(c, a, clean=i == 0) for i, (c, a) in enumerate(zip(commons, arms))]
    pins = [{'path': str(p), 'ROM_sha256': sha(p.read_bytes()), 'ARM9_sha256': sha(a), 'COMMON_sha256': sha(c)}
            for p, a, c in zip(paths, arms, commons)]
    sources = []
    for n in range(960, 992):
        source, canonical, current = [e[n] for e in entries]
        refs = [{**asdict(e), 'text': None} for e in (source, current)]
        sources.append({'id': n, 'source_hex': source.text.hex(), 'Japanese': source.text.decode('cp932'),
                        'canonical_hex': canonical.text.hex(), 'current_hex': current.text.hex(),
                        'current_English': current.text.decode('cp932'),
                        'source_reference': refs[0], 'current_reference': refs[1]})
    save(ROOT / 'source_and_neighbors.json', {'pins': pins, 'rows': sources,
                                             'adjacent_storage_does_not_establish_scene_sequence': True})
    context = read(ROOT / 'native_context.json')
    assert context['candidate_sha256'] == pins[2]['ROM_sha256']
    by_id = {r['id']: r for r in sources}
    voice_map = {n: (table, voice) for table, ids in TABLES.items() for voice, n in enumerate(ids) if n != -1}
    rows = []
    for n, text in TEXTS.items():
        s = by_id[n]
        assert text.isascii() and not re.search(r'\s{2,}', text)
        assert text.count('%s') == s['Japanese'].count('%s') == (2 if 978 <= n <= 983 else 0)
        if n < 972:
            meaning = 'Will make the remaining arrangements; awaits or wonders about the result. Does not announce successful execution.'
            if n in (967, 970): meaning += ' Specifically hopes or wonders whether it will go well.'
            elif n == 965: meaning += ' Invites waiting for good news.'
            else: meaning += ' Expresses anticipation or curiosity about the eventual outcome.'
            scene = 'Original57384 checks successful scheduling return;57390-57398 role2 narration precedes XP/gold deduction. This is acceptance/arrangement,not proof of the future scheme outcome.'
            note = 'Retain already natural wording and each voice\'s anticipation/uncertainty. Normalize full-width Latin I through the established literal paragraph path; do not invent a successful result.'
        elif n == 972:
            meaning = 'The regular ship due in port this month apparently sank after encountering a storm; presented as hearsay.'
            scene = 'Separate original579C4-57A38 barmaid/NPC rumor. Original town condition5..11 permits this follow-up after a condition report. Not a scheme result or a universal scheduled disaster.'
            note = 'Use regular run for 定期船 and apparently for hearsay. Preserve the monthly due arrival and sinking/storm; do not add a named ship,cargo,piracy or certainty.'
        elif n <= 977:
            meaning = 'Ask which town\'s broker to bribe.'
            scene = 'Original57104 action9 branch at57150-57158,role2 narration,before the target faction\'s eligible-town selector.'
            note = 'Keep broker as established scheme terminology and the town-selection question. Voice2 retains planned intent;the elder voice uses natural shall. Youthful katakana does not authorize a fabricated misspelling.'
        elif n <= 983:
            meaning = 'Confirm bribing the broker belonging to the selected faction in the selected town;TOWN first,FACTION second.'
            scene = 'Original56A10-56A50 obtains town name then target-faction name and calls role2 yes/no wrapper. Other skill branch uses an existing generic uncertain-chance confirmation.'
            note = 'Keep native TOWN then FACTION arguments and possessive broker. Turn awkward imperative fragments into complete natural confirmations,without inventing a price or guaranteed success.'
        else:
            meaning = 'The Tavern is too crowded for a private conversation;return another day or later.'
            if n == 988: meaning = 'The Tavern is too crowded for a private conversation;explicitly suggests tomorrow.'
            elif n in (984, 987): meaning += ' Specifically says no suitable seat is available and addresses the admiral.'
            scene = 'Original572D0 private-meeting availability failure at572F4-572FC role2 narration;returns before scheme selection and gold deduction.'
            note = 'Preserve seats where explicit,admiral where explicit,and tomorrow only for988. Other voices do not invent a specific date. Crowded refusal is a separate selection,not dialogue concatenated after the arrangement reply.'
        table, voice = voice_map.get(n, (None, None))
        rows.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n,
                     'interaction_group': f'Tavern-followup-table-{table:08X}' if table else 'Tavern-condition-followup-rumor',
                     'source_hex': s['source_hex'], 'japanese': s['Japanese'], 'source_reference': s['source_reference'],
                     'canonical_source_hex': s['canonical_hex'], 'current_text_hex': s['current_hex'],
                     'current_English': s['current_English'], 'current_reference': s['current_reference'],
                     'english': text + '{PAD}', 'source_meaning': meaning,
                     'speaker': f'Original role2 Strategist,voice slot{voice}' if table else 'Original selected town barmaid/NPC',
                     'context': scene, 'localization_note': note, 'source_voice_table': table, 'source_voice_slot': voice,
                     'source_native_arguments': ['town', 'faction'] if 978 <= n <= 983 else [],
                     'English_argument_source_indices': [0, 1] if 978 <= n <= 983 else [],
                     'decision': 'retain' if ' '.join(s['current_English'].replace('\uff29', 'I').split()) == text else 'revise',
                     'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False},
                     'status': 'source-context-prose-reviewed-NOT-integrated'})
    save(MANUSCRIPT, {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
                      'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US',
                      'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                      'file_path': '/COMMON/MESFILE.DK4', 'source_pins': pins,
                      'native_context_proof': str(ROOT / 'native_context.json'),
                      'status': 'source-context-prose-reviewed-NOT-playable', 'records': rows,
                      'producer_sha256': sha(Path(__file__).read_bytes())})
    print(f'25 source/context/prose drafts: {sum(r["decision"] == "revise" for r in rows)} revised;formatting/integration pending.', flush=True)


if __name__ == '__main__':
    main()
