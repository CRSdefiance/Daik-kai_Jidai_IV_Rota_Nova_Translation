"""Revisit the shore reports and whale sighting in their complete event groups."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import register_deck_phrase_wraps_20261121 as parent
from scripts import stage_bubble_portrait_wraps_20261120 as portrait
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment


base = parent.base
ARM, COMMON, CLEAN = portrait.ARM, portrait.COMMON, portrait.CLEAN
ROOT = Path('work/shore_phrase_wraps_20261121')
ROM, PROOF = ROOT / 'Shore_Phrase_Wraps_STAGED.nds', ROOT / 'staged.json'
PATCH, REBUILT = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
CHECKPOINTS = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
CONTEXTS = tuple(CHECKPOINTS / f'{name}_context_v1.json' for name in ('crew_and_shore_reports', 'oasis_and_whale_reports'))
TRIAGE = CHECKPOINTS / 'shared_ascii_early_break_triage_20261121_v2.json'
BASE = 0x02000000
GROUP_STARTS = (2234, 2239, 2243, 2258, 2264, 2308, 2352)
LEADS = {2237, 2249, 2264, 2265, 2267, 2311, 2357}
EDITS = {
    2237: ("The locals seem friendly. I think we'll be welcome. Shall we go now, Admiral?", ["The locals seem friendly.","I think we'll be welcome.","Shall we go now, Admiral?"],
           "Keep the friendly reception tentative and give the older officer a whole question to invite the admiral ashore."),
    2243: ("Bad news! The locals attacked our expedition!", ["Bad news!","The locals attacked our expedition!"],
           "Retain the direct alarm and give the report a complete row instead of breaking the subject from the attack."),
    2249: ("The locals have attacked our party!", [],
           "Keep the immediate report and identify both the attackers and the expedition party."),
    2264: ("Admiral! Disease has swept the ship! It seems the expedition caught it when the animals attacked!", ["Admiral! Disease has swept the ship!","It seems the expedition caught it","when the animals attacked!"],
           "Preserve the shipwide outbreak and the officer's tentative account of the expedition's exposure."),
    2265: ("Admiral! Sickness all over the ship! Looks like the party caught it when those animals attacked!", ["Admiral! Sickness all over the ship!","Looks like the party caught it","when those animals attacked!"],
           "Use the lookout's familiar alarm. Keep the apparent connection to the animal attack separate from the certain outbreak."),
    2266: ("Disease has swept through the ship! Looks like the expedition caught it when those beasts attacked!", ["Disease has swept through the ship!","Looks like the expedition caught it","when those beasts attacked!"],
           "Keep the emphatic older voice, the outbreak aboard and the apparent link to the beasts."),
    2267: ("This is bad! Sickness everywhere! They say it spread from the people the animals attacked!", ["This is bad! Sickness everywhere!","They say it spread from the people","the animals attacked!"],
           "Keep the young lookout's alarm and the reported transmission from the people who were attacked."),
    2311: ("Admiral, trouble! I hear our expedition's stuck in a bottomless bog!", ["Admiral, trouble!","I hear our expedition's stuck","in a bottomless bog!"],
           "Keep the urgent call, hearsay and bottomless bog together in whole phrases."),
    2353: ("Oh, the white whale's escaping... What's that?! I see a glint where it dived!", ["Oh, the white whale's escaping...","What's that?!","I see a glint where it dived!"],
           "Keep the interrupted escape report and the surprised discovery at the same place."),
    2355: ("Aw, it got away... Oh? There's something shining where the white whale dived!", ["Aw, it got away... Oh?","something shining","where the white whale dived!"],
           "Keep the disappointment, discovery and dive location. Keep the white whale together on the same line."),
    2357: ("Hm, seems the white whale escaped... Wait! A glint where it dove!", ["Hm, seems the white whale escaped...","Wait! A glint where it dove!"],
           "The older voice first makes a tentative observation and then notices the glint at the dive site. Keep the change of attention between rows."),
}
RETAIN = {
    2234: 'The opening already says how the officer heard of the welcome, and the final call reads briskly.',
    2235: 'The warm invitation and informal encouragement suit the speaker.',
    2236: 'The passive report preserves the sense of an invitation relayed by others.',
    2238: 'The eager voice speaks of the invitation as already given and wants to go immediately.',
    2239: 'The follow-up identifies both supplies and who shared them.',
    2240: 'The existing wording keeps both staples and the officer’s simple gratitude.',
    2241: 'The line names food and water in the formal follow-up.',
    2242: 'Keeping “shared” preserves the friendly exchange.',
    2244: 'The brief report gives the attacker and the target on one line.',
    2245: 'The voiced alarm and hearsay distinguish this account from a direct witness.',
    2246: 'The rough voice addresses the admiral immediately and calls the expedition “our party.”',
    2247: 'The complete attack report and the older voice’s condemnation get separate beats.',
    2248: 'The relief about being eaten is the young speaker’s dark joke after the reported attack.',
    2258: 'The reported attack is tentative and names wild animals as the apparent cause.',
    2259: 'The short exclamation suits an immediate report about the speaker’s own party.',
    2260: 'The officer addresses the admiral and qualifies the report.',
    2261: 'The emphatic call begins a confident report from the rougher voice.',
    2262: 'The officer explicitly relays the news of a wild animal attack.',
    2263: '“Wild beasts” keeps the older voice’s emphatic vocabulary.',
    2268: 'This formal speaker treats the spread from the expedition as confirmed.',
    2308: '“It seems” preserves the reported danger, and the complete location stays together.',
    2309: 'The officer’s “appears” keeps the measured uncertainty.',
    2310: 'The relaxed wording suits this voice while retaining the bottomless bog.',
    2312: 'The rough speaker leads with a warning and follows with qualified information.',
    2313: 'The alarm preserves the older voice’s explicit uncertainty about the expedition.',
    2314: 'The concise cry and present-tense report retain the younger voice’s urgency.',
    2352: 'The pause after the escape leaves room for the lookout to notice the light.',
    2354: 'The dismay and quick, informal “Hey” preserve the swing to surprise.',
    2356: 'The rough voice keeps the sudden question and a whole description of the light on its own line.',
    2358: 'The younger voice opens with disappointment and ends by pointing out the glow.',
}


def groups_and_records(clean, arm):
    groups, history = {}, {}
    for path in CONTEXTS:
        doc = base.load(path)
        assert doc['source_ROM_sha256'] == base.digest(CLEAN)
        for group in doc['native_context']:
            if group['first_ID'] not in GROUP_STARTS:
                continue
            at = group['table'] - BASE
            assert tuple(group['slots']) == unpack_from('<8i', clean, at) == unpack_from('<8i', arm, at)
            caller, = group['native_callers']
            lo, hi = caller['load_PC'] - BASE, caller['call_PC'] - BASE + 4
            assert clean[lo:hi] == arm[lo:hi] == bytes.fromhex(caller['clean_and_current_hex'])
            literal = caller['literal_address'] - BASE
            assert unpack_from('<I', clean, literal) == unpack_from('<I', arm, literal) == (group['table'],)
            assert caller['consumer'] == BASE + 0x53D44
            group = group | {'consumer': caller['consumer']}
            for n in range(group['first_ID'], group['last_ID'] + 1):
                groups[n] = group
        history.update({row['message_ID']: (row, path) for row in doc['records']})
    assert len(groups) == 41 and groups.keys() == EDITS.keys() | RETAIN.keys()
    assert EDITS.keys().isdisjoint(RETAIN)
    return groups, history


def main():
    assert not PROOF.exists()
    release, ledger = map(base.load, (parent.RELEASE, base.LEDGER))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(parent.ROM) == release['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    runtime = portrait.RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    arm, common = runtime.arm, runtime.common
    clean = base.NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    source = portrait.common_message_entries(clean.read_file(COMMON), clean_arm)
    previous = portrait.owned_entries(common, arm, sha256(arm[portrait.DIRECTORY_OFFSET:portrait.TABLE_OFFSET]).hexdigest())
    groups, history = groups_and_records(clean_arm, arm)
    triage = base.load(TRIAGE)
    assert triage['candidate_sha256'] == release['candidate_sha256']
    flagged = {r['message_ID']: r for r in triage['records']}
    assert flagged.keys() & groups.keys() == LEADS == flagged.keys() & EDITS.keys()
    credited = {(r['file_path'], r['id']) for r in ledger[base.CONTEXT]['integrated_record_keys']}
    rows = {}
    for n, group in sorted(groups.items()):
        prior, path = history[n]
        clean_row, current = source[n], previous[n]
        assert (COMMON, prior['id']) in credited and clean_row.text.hex() == prior['source_hex']
        assert prior['original_substitution_count'] == 0 and all(b'%' not in r.text for r in (clean_row, current))
        if n in flagged:
            original = flagged[n]
            assert clean_row.text.hex() == original['clean_hex'] and current.text.hex() == original['current_hex']
            assert portrait.reference(clean_row) == original['clean_reference']
            assert portrait.reference(current) == original['current_reference']
        old = portrait.unwrapped(current.text)
        assert old == prior['english'], (n, old, prior['english'])
        english, phrases, note = EDITS[n] if n in EDITS else (old, (), RETAIN[n])
        rows[n] = dict(id=prior['id'], file_path=COMMON, message_ID=n, speaker=prior['speaker'], context=prior['context'],
                       source_meaning=prior['source_meaning'], clean_Japanese=clean_row.text.decode('cp932'),
                       source_reference=portrait.reference(clean_row), current_reference=portrait.reference(current),
                       source_hex=clean_row.text.hex(), current_hex=current.text.hex(), previous_English=old,
                       english=english, protected_phrases=phrases, localization_note=note,
                       decision='revision' if english != old else 'wrap revision' if n in EDITS else 'retention',
                       original_substitution_count=0, prior_context=str(path), original_role=group['original_role_argument'],
                       original_table=group['table'], review=dict.fromkeys(portrait.GATES, True))
    wrap = FunctionType(portrait.compile_layouts.__code__, portrait.compile_layouts.__globals__ | {
        'PHRASES': {n: phrases for n, (_, phrases, _) in EDITS.items() if phrases},
    })
    edited = wrap({n: rows[n] for n in EDITS})
    assert all(previous[n].text != text for n, text in edited.items())
    new_common, installed, allocation = owned_deployment(common, arm, previous, edited)
    pending = base.load(parent.PENDING)['records']
    for row in pending:
        rebound = installed[row['message_ID']]
        assert portrait.reference(rebound) == row['current_reference'] and rebound.text.hex() == row['current_hex']

    ctx = portrait.with_components(runtime, arm, new_common)
    painter, _, font = portrait.font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    pages = []
    for n, row in rows.items():
        group = groups[n]
        actor = next(a for a, _, message in group['original_voice_choices'] if message == n)
        payload = installed[n].text
        native = portrait.portrait_case(ctx, row, group, payload, actor)
        display = native.pop('display')
        lines = [line.strip() for line in display.decode('ascii').splitlines()]
        assert 1 <= len(lines) <= 4 and portrait.unwrapped(display) == row['english']
        assert all(any(phrase in line for line in lines) for phrase in row['protected_phrases'])
        ink, glyphs = portrait.render_portrait(painter, arm, kanji, display)
        codes = [g['code'] for g in glyphs]
        assert codes == portrait.glyph_codes(display)
        assert codes[0] == ord(row['english'][0]) and codes[-1] == ord(row['english'][-1])
        row.update(staged_hex=payload.hex(), staged_reference=portrait.reference(installed[n]),
                   native=native, visible_lines=lines, display_hex=display.hex(),
                   native_ink_sha256=sha256(ink).hexdigest(), glyph_count=len(codes), expected_pages=1)
        if n in edited:
            pages.append((n, ink))
            print(n, lines, flush=True)

    image = base.NdsImage.open(parent.ROM)
    image.replace_file(COMMON, new_common)
    target = bytes(image.rom.save())
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    if ROM.exists():
        assert ROM.read_bytes() == target
    else:
        ROM.write_bytes(target)
    if not PATCH.exists():
        make_xdelta(CLEAN, ROM, PATCH)
    if not REBUILT.exists():
        apply_xdelta(CLEAN, PATCH, REBUILT)
    assert REBUILT.read_bytes() == target
    proof = dict(candidate_sha256=base.digest(ROM), parent_sha256=release['candidate_sha256'],
                 clean_input_sha256=release['clean_input_sha256'], target_ARM9_sha256=sha256(arm).hexdigest(),
                 target_COMMON_sha256=sha256(new_common).hexdigest(), full_parent_inverse=True, allocation=allocation,
                 translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1', target_locale='en-US',
                 review_gates=list(portrait.GATES), records=list(rows.values()), sheets=portrait.portrait_sheets(ROOT, pages),
                 font=font, patch_sha256=base.digest(PATCH), unchanged_pending_records=len(pending),
                 source_receipts={str(path): base.digest(path) for path in (*CONTEXTS, TRIAGE)},
                 staged_reconstruction_byte_exact=True, gameplay_pending=True, new_contextual_credit=0)
    validate_natural_dialogue_batch(proof)
    base.save(PROOF, proof)


if __name__ == '__main__':
    main()

