"""Review the remaining early wraps in mutiny, navigation, Search and Refit text."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import checkpoint_navigation_prerequisite_review_v1 as nav
from scripts import register_item_advice_phrase_wraps_20261121 as parent
from scripts import register_mutiny_dialogue_followup_20261119 as mutiny_release
from scripts import register_shark_encounter_v1 as shark_release
from scripts import stage_mutiny_dialogue_followup_20261119 as mutiny
from scripts import stage_bubble_portrait_wraps_20261120 as portrait
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = parent.base, parent.batch
ARM, COMMON, CLEAN = portrait.ARM, portrait.COMMON, portrait.CLEAN
ROOT = Path('work/final_early_wrap_leads_20261121')
ROM, PROOF = ROOT / 'Early_Wrap_Leads_STAGED.nds', ROOT / 'staged.json'
PATCH, REBUILT = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
CHECKPOINTS = parent.stage.CHECKPOINTS
TRIAGE = CHECKPOINTS / 'shared_ascii_early_break_triage_20261121_v5.json'
PENDING = CHECKPOINTS / 'shared_display_worklist_20261121_v2.json'
REFIT_SOURCE = CHECKPOINTS / 'refit_help_wraps_context_20261115_v1.json'
FAMILIES = {
    mutiny.source.OUTPUT: range(542, 548),
    nav.OUTPUT: range(637, 645),
    CHECKPOINTS / 'shark_encounter_context_v2.json': range(2443, 2454),
    REFIT_SOURCE: (*range(1247, 1256), *range(1272, 1275)),
}
PORTRAIT_IDS = {n for path, items in FAMILIES.items() if path != REFIT_SOURCE for n in items}
REFIT_IDS = set(FAMILIES[REFIT_SOURCE])
EDITS = {
    547: ("Admiral! Without a Boarding Leader, we can't get the crew to listen!",
          ("Admiral! Without a Boarding Leader,", "we can't get the crew to listen!"),
          'The young voice addresses the admiral and makes the missing Boarding Leader the condition. Keep its complete conclusion on one row.'),
    640: ("No route to that port, I'm afraid.", (),
          'Retain the Surveyor’s polite regret and the destination. The complete warning fits one line.'),
    1253: ("A missionary eases sailors' discontent. You can also hand out trade goods in the Square.",
           ("sailors' discontent.", 'You can also hand out', 'trade goods in the Square.'),
           'Keep both benefits and make the option to distribute trade goods a separate sentence.'),
    1273: ("A stern gun fires astern, but its aim is poor.", (),
           'Keep the rearward direction and the gun’s poor accuracy. The bow gun’s separate drawback is reduced power.'),
    2449: ("Why don't we raise it and find out?", (),
           'Samwell makes a casual proposal to test his idea. The short question leaves room for Al’s immediate objection.'),
}


def refit_compiler(text):
    phrases = next((phrases for n, (wording, phrases, _) in EDITS.items() if n in REFIT_IDS and wording == text), ())
    marked = text
    for phrase in phrases:
        assert marked.count(phrase) == 1
        marked = marked.replace(phrase, phrase.replace(' ', '_'))
    raw, lines = compile_paragraph(marked)
    lines = [line.replace('_', ' ') for line in lines]
    assert ' '.join(lines) == text and all(any(phrase in line for line in lines) for phrase in phrases)
    return raw.replace(b'_', b' '), lines


def sources(clean, arm):
    prior, groups = {}, {}
    for path, ids in FAMILIES.items():
        doc = base.load(path)
        doc_rows = {r.get('message_ID', r.get('message_id')): r for r in doc['records']}
        prior.update({n: (doc_rows[n], path) for n in ids})
        if path == mutiny.source.OUTPUT:
            bound = mutiny.group_map(doc, clean, arm)
            groups.update({n: (bound[n], mutiny.actors(bound[n], n)[0]) for n in ids})
        elif path == nav.OUTPUT:
            nav.bind_predicate(clean, arm)
            group, = [g for g in doc['exact_native_groups'] if g['first_ID'] == 637]
            table = group['table'] - nav.BASE
            assert clean[table:table + 32] == arm[table:table + 32]
            groups.update({n: (group, next(actor for actor, _, message in group['original_voice_choices'] if message == n))
                           for n in ids})
        elif path != REFIT_SOURCE:
            from scripts import review_shark_encounter_v1 as shark
            assert arm[shark.START:shark.STOP] == clean[shark.START:shark.STOP]
            for n in ids:
                row = doc_rows[n]
                if 'captain_index' in row:
                    group, = [g for g in doc['captain_tables'] if n in g['table_slots']]
                    actor = row['captain_index']
                    assert group['table_slots'][actor] == n
                    groups[n] = group | {'original_role_argument': None}, actor
                else:
                    groups[n] = dict(consumer=0x02053FE4, table=n, original_role_argument=None), row['original_actor_ID']
    revised, = [r for r in base.load(mutiny_release.REVIEW)["records"] if r["message_ID"] == 544]
    prior[544] = (revised, mutiny_release.REVIEW)
    revised, = [r for r in base.load(shark_release.REVIEW)["records"] if r.get("message_ID", r.get("message_id")) == 2448]
    prior[2448] = (revised, shark_release.REVIEW)
    return prior, groups


def refit_native():
    """Re-execute the proven initialized Refit painter for the changed paragraphs."""
    from scripts import verify_refit_editorial_v830 as original
    fields = base.load(PROOF)
    native = ROOT / 'refit_native'
    source = checked_text(getsource(original.main), {
        "    target = NdsImage.open(ROM).read_file('/__arm9__.bin')":
            "    manuscript['records'] = [row | {'message_id': row['message_ID'], 'editorial_decision': row['decision']}\n"
            "                             for row in manuscript['records'] if row['message_ID'] in (1253, 1273)]\n"
            "    assert len(manuscript['records']) == 2\n"
            "    target = NdsImage.open(ROM).read_file('/__arm9__.bin')",
        'previews.mkdir(exist_ok=True)': 'previews.mkdir(parents=True)',
        '(line_index * 12 + y) * 168': '(line_index * 12 + y + 1) * 168',
        'All31 current native fonts/independent complete planes/guards pass;four sheets await visual review.':
            'Both revised Refit paragraphs passed complete native pixel and buffer guard checks.',
    })
    scope = vars(original) | dict(ROM=ROM, ROOT=native, MANUSCRIPT=PROOF, compile_paragraph=refit_compiler)
    assert fields['current_candidate_sha256'] == base.digest(ROM)
    exec(compile(source, __file__ + '::refit-geometry', 'exec'), scope)
    scope['main']()


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
    clean_rows = portrait.common_message_entries(clean.read_file(COMMON), clean_arm)
    old = portrait.owned_entries(common, arm, sha256(arm[portrait.DIRECTORY_OFFSET:portrait.TABLE_OFFSET]).hexdigest())
    prior, groups = sources(clean_arm, arm)
    triage = base.load(TRIAGE)
    assert triage['candidate_sha256'] == release['candidate_sha256']
    flagged = {r['message_ID']: r for r in triage['records']}
    assert flagged.keys() == EDITS.keys() | {117}
    unbound = flagged[117]
    assert clean_rows[117].text.hex() == unbound['clean_hex'] and old[117].text.hex() == unbound['current_hex']
    rows = {}
    credited = {(r['file_path'], r['id']) for r in ledger[base.CONTEXT]['integrated_record_keys']}
    for n, (record, path) in sorted(prior.items()):
        original, installed = clean_rows[n], old[n]
        assert record['id'] == f'COMMON_MESSAGE_{n}' and (COMMON, record['id']) in credited
        assert record.get('source_hex', record.get('exact_clean_hex')) == original.text.hex()
        assert b'%' not in original.text and b'%' not in installed.text
        current = portrait.unwrapped(installed.text)
        assert record['english'] == current, (n, current, record['english'])
        if n in flagged:
            lead = flagged[n]
            assert portrait.reference(original) == lead['clean_reference'] and portrait.reference(installed) == lead['current_reference']
            assert original.text.hex() == lead['clean_hex'] and installed.text.hex() == lead['current_hex']
        english, phrases, note = EDITS.get(n, (current, (), record['localization_note']))
        rows[n] = dict(id=record['id'], file_path=COMMON, message_ID=n, speaker=record['speaker'], context=record['context'],
                       source_meaning=record['source_meaning'], clean_Japanese=original.text.decode('cp932'),
                       source_reference=portrait.reference(original), current_reference=portrait.reference(installed),
                       source_hex=original.text.hex(), current_hex=installed.text.hex(), previous_English=current,
                       english=english, protected_phrases=phrases, original_substitution_count=0,
                       localization_note=note, decision='revision' if n in EDITS else 'retention',
                       review=dict.fromkeys(portrait.GATES, True), prior_context=str(path))

    wrap = FunctionType(portrait.compile_layouts.__code__, portrait.compile_layouts.__globals__ |
                        {'PHRASES': {n: v[1] for n, v in EDITS.items() if n in PORTRAIT_IDS and v[1]}})
    edited = wrap({n: rows[n] for n in EDITS.keys() & PORTRAIT_IDS})
    edited.update({n: refit_compiler(rows[n]['english'])[0][:-1] for n in EDITS.keys() & REFIT_IDS})
    assert all(old[n].text != text for n, text in edited.items())
    common_new, installed, allocations = owned_deployment(common, arm, old, edited)
    runtime_new = portrait.with_components(runtime, arm, common_new)
    painter, _, _ = portrait.font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    pages = []
    for n, row in rows.items():
        payload = installed[n].text
        row.update(staged_hex=payload.hex(), staged_reference=portrait.reference(installed[n]), expected_pages=1)
        if n in REFIT_IDS:
            compiled, lines = refit_compiler(row['english'])
            assert compiled == payload + b'\0'
            row['visible_lines'] = lines
            continue
        group, actor = groups[n]
        case = portrait.portrait_case(runtime_new, row, group, payload, actor)
        display = case.pop('display')
        lines = [line.strip() for line in display.decode('ascii').splitlines()]
        assert 1 <= len(lines) <= 4 and portrait.unwrapped(display) == row['english']
        ink, glyphs = portrait.render_portrait(painter, arm, kanji, display)
        assert [g['code'] for g in glyphs] == portrait.glyph_codes(display)
        assert (glyphs[0]['code'], glyphs[-1]['code']) == (ord(row['english'][0]), ord(row['english'][-1]))
        assert all(any(phrase in line for line in lines) for phrase in row['protected_phrases'])
        row.update(display_hex=display.hex(), visible_lines=lines, native=case, ink_sha256=sha256(ink).hexdigest())
        if n in EDITS:
            pages.append((n, ink))

    pending = base.load(PENDING)['records']
    shifted = {}
    for row in pending:
        n = row['message_ID']
        a, b = row['current_reference'], portrait.reference(installed[n])
        assert portrait.reference(old[n]) == a and installed[n].text.hex() == row['current_hex']
        assert a | {'record_index': b['record_index']} == b
        if a != b:
            shifted[n] = dict(before=a, after=b)
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(COMMON, common_new)
    target = bytes(image.rom.save())
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(target)
    make_xdelta(CLEAN, ROM, PATCH)
    apply_xdelta(CLEAN, PATCH, REBUILT)
    assert REBUILT.read_bytes() == target
    digest = base.digest(ROM)
    proof = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
                 review_gates=list(portrait.GATES), records=list(rows.values()), source_receipts={str(f): base.digest(f) for f in (*FAMILIES, mutiny_release.REVIEW, shark_release.REVIEW, TRIAGE, PENDING)},
                 candidate_sha256=digest, current_candidate_sha256=digest, research_ROM_sha256=digest,
                 parent_sha256=release['candidate_sha256'], exact_clean_reconstruction=True,
                 patch_sha256=base.digest(PATCH), whole_parent_inverse=True,
                 target_ARM9_sha256=batch.digest(arm), target_COMMON_sha256=batch.digest(common_new),
                 sheets=portrait.portrait_sheets(ROOT, pages), allocations=allocations,
                 unchanged_pending=len(pending), pending_index_shifts=shifted,
                 retained_legacy_117=dict(status='display owner unconfirmed', original_reference=unbound,
                                          exact_reference_after=portrait.reference(installed[117])),
                 new_contextual_credit=0)
    validate_natural_dialogue_batch(proof)
    base.save(PROOF, proof)
    refit_native()


if __name__ == '__main__':
    main()


