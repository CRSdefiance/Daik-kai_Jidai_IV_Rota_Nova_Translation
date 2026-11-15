"""Resolve a spoken bridge cue and check FE wrapping before rendering the batch."""
from pathlib import Path
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import Rafael_B45_FE_source_painter_v7894 as fe
from scripts import square_shopkeeper_font_oracles_v7020 as old_font
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.plan_rafael_B301_B320_v1 import FORMATTING, PREFERENCES, ROOT, SOURCE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_rafael_B301_B320_clean_v1 import digest
from scripts.write_rafael_B301_B320_contextual_v1 import OUT


PROSE = OUT.with_name('rafael_B301_B320_contextual_review_v2.json')
MANUSCRIPT = ROOT / 'ordinary_formatting_manuscript_v2.json'
PREFS = ROOT / 'ordinary_visual_preferences_v2.json'
PROBE = ROOT / 'FE_width_probe_v1.json'
BRIDGE = 'DK4_MES_B305_R0198'
BRIDGE_ENGLISH = "What's got you so scared? Hurry up and cross!"
BRIDGE_REASON = "Keep Claudio's teasing question and restore his explicit order to cross the bridge."


def main():
    assert not any(path.exists() for path in (PROSE, MANUSCRIPT, PREFS, PROBE))
    prose, doc, plan, prefs = map(load, (OUT, FORMATTING, SOURCE, PREFERENCES))
    assert plan['manuscript_sha256'] == digest(FORMATTING) and not plan['failures']
    planned = {row['id']: row for row in plan['records']}
    assert planned[BRIDGE]['lines'] == ['What are you so scared of?', 'Get moving!']
    assert [i['code'] for i in planned[BRIDGE]['base_QA']['issues'] if i['severity'] != 'info'] == ['weak-line-ending']
    for row in prose['records'] + doc['records']:
        if row['id'] != BRIDGE:
            continue
        assert row['english'] == 'What are you so scared of? Get moving!'
        row.update(english=BRIDGE_ENGLISH, finding=BRIDGE_REASON, localization_note=BRIDGE_REASON)
        if 'planned_English_markup' in row:
            row['planned_English_markup'] = '{SPEAKER:05}' + BRIDGE_ENGLISH
            row['editorial_logical_English'] = BRIDGE_ENGLISH
    prose.update(previous_contextual_version=str(OUT), previous_contextual_sha256=digest(OUT),
                 single_source_qualified_bridge_refinement=BRIDGE)
    save(PROSE, prose)
    doc.update(manuscript_sha256=digest(PROSE), parent_contextual_proof=str(PROSE))
    save(MANUSCRIPT, doc)

    runtime = doc['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=0)
    assert ctx.receipt() == runtime
    ascii_factory = FunctionType(old_font.make_painter.__code__,
        {**old_font.make_painter.__globals__, 'CURRENT_ARM9': sha(ctx.arm)})
    factory = FunctionType(fe.make_source_painter.__code__,
        {**fe.make_source_painter.__globals__, 'CURRENT_ARM9': sha(ctx.arm), 'ASCII_painter': ascii_factory})
    paint, _ = factory(ctx.image)
    manuscript = {row['id']: row for row in doc['records']}

    def prefer(ident, **rule):
        row = manuscript[ident]
        prefs['records'][ident] = {**rule, 'bindings': {
            key: sha(row[key].encode('utf-8')) for key in ('source_hex', 'current_hex', 'english')
        }}

    prefer('DK4_MES_B309_R0059', line_phrases=['hidden Christian village.', 'in the Mediterranean.'],
           page_clause='You can probably find a map in a town somewhere in the Mediterranean.',
           reason='Keep the settlement name intact and carry the complete map lead to the next page.')
    prefer('DK4_MES_B313_R0050', line_phrases=["I didn't listen too closely."],
           page_clause="so I didn't listen too closely.",
           reason='Keep Safia’s dismissal in a full clause across the page turn.')
    records = []
    for row in plan['records']:
        if row['kind'] != 'system-FE':
            continue
        ident = row['id']
        raw = bytes.fromhex(row['encoded_hex'])
        parity = (len(raw)-len(bytes.fromhex(manuscript[ident]['current_hex']))) % 2
        display = paint(raw[1:])
        stored = paint(raw[1:]+b' '*parity) if parity else display
        entry = dict(id=ident, compiled_hex=raw.hex(), parity_space_required=bool(parity),
                     compiled_plane_sha256=sha(display['physical']), parity_plane_sha256=sha(stored['physical']))
        try:
            check_FE_rows(raw[1:], display)
        except AssertionError:
            assert max(map(len, raw[1:].split(b'\n'))) >= 37
            prefer(ident, FE_planning_cells=36,
                   reason='The original FE painter uses an extra row at the initially planned width.')
            entry['compiled_reflow_required'] = True
        else:
            try:
                check_FE_rows(raw[1:]+b' '*parity, stored)
            except AssertionError:
                assert parity
                if (display['physical'], display['logical']) == (stored['physical'], stored['logical']):
                    assert stored['events'][:len(display['events'])] == display['events']
                    extra = stored['events'][len(display['events']):]
                    assert extra and all(event['code'] == 32 for event in extra)
                    entry['stored_zero_ink_events_need_exact_check'] = extra
                else:
                    prefer(ident, FE_planning_cells=36,
                           reason='Storage padding moves visible text to an extra row in the native FE painter.')
                    entry['stored_reflow_required'] = True
        records.append(entry)
    assert len(records) == 16
    save(PROBE, dict(runtime=runtime, initial_plan_sha256=digest(SOURCE), records=records,
                     no_ROM_written=True, final_storage_checks_pending=True, new_credit=0))
    prefs.update(FE_probe=str(PROBE), FE_probe_sha256=digest(PROBE))
    save(PREFS, prefs)
    print('Checked all 16 FE paragraphs and bound the three progressive layout findings.')


if __name__ == '__main__':
    main()
