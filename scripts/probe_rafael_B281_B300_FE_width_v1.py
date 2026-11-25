"""Identify exact FE right-edge cases before the complete native-page run."""
from pathlib import Path
from types import FunctionType

from scripts.audit_story_glyph_consistency import load, save
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B281_B300_v1 import FORMATTING, PREFERENCES, ROOT
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts import Rafael_B45_FE_source_painter_v7894 as fe
from scripts import square_shopkeeper_font_oracles_v7020 as old_font
from dk4tool.patch.grand_race_menu_release import sha


PLAN = ROOT/'initial_plan_v1/automatic_plans.json'
OUT = ROOT/'FE_width_probe_v1.json'
PREFS = ROOT/'ordinary_visual_preferences_v2.json'
WIDTH_IDS = {'DK4_MES_B281_R0054', 'DK4_MES_B287_R0051'}
MALACCA = 'DK4_MES_B284_R0054'


def main():
    assert not OUT.exists() and not PREFS.exists()
    doc, plan, prefs = map(load, (FORMATTING, PLAN, PREFERENCES))
    assert plan['manuscript_sha256'] == digest(FORMATTING)
    rt = doc['runtime']
    ctx = RegisteredRuntime(rt['release_proof'], rt['startup_proof'], captain=0)
    assert ctx.receipt() == rt
    ascii_factory = FunctionType(old_font.make_painter.__code__,
        {**old_font.make_painter.__globals__, 'CURRENT_ARM9': sha(ctx.arm)})
    factory = FunctionType(fe.make_source_painter.__code__,
        {**fe.make_source_painter.__globals__, 'CURRENT_ARM9': sha(ctx.arm), 'ASCII_painter': ascii_factory})
    paint, _ = factory(ctx.image)
    manuscript = {row['id']: row for row in doc['records']}
    records = []
    for row in plan['records']:
        if row['kind'] != 'system-FE':
            continue
        ident = row['id']
        original = manuscript[ident]
        raw = bytes.fromhex(row['encoded_hex'])
        parity = (len(raw)-len(bytes.fromhex(original['current_hex']))) % 2
        rendered = paint(raw[1:])
        stored = paint(raw[1:]+b' '*parity) if parity else rendered
        receipt = dict(id=ident, compiled_hex=raw.hex(), parity_space_required=bool(parity),
                       compiled_plane_sha256=sha(rendered['physical']), parity_plane_sha256=sha(stored['physical']))
        if ident in WIDTH_IDS:
            assert any(event['y'] > 0 and event['code'] != 32 for event in rendered['events'])
            assert len(raw) == 38 and not parity
            receipt['one_row_would_move_visible_final_glyph'] = True
            prefs['records'][ident] = dict(FE_planning_cells=36, line_phrases=['rose slightly'],
                reason='The native painter moves visible text to another row at the original planned width.',
                bindings={key: sha(original[key].encode('utf-8')) for key in ('source_hex','current_hex','english')})
        elif ident == MALACCA:
            assert parity and raw[1:] == b'Your share in Malacca rose slightly!'
            assert rendered['physical'] == stored['physical'] and rendered['logical'] == stored['logical']
            assert stored['events'][:-2] == rendered['events']
            assert stored['events'][-2:] == [dict(kind='ascii', code=32, style=15, x=x, y=12) for x in (0,6)]
            receipt['two_exact_stored_zero_ink_events'] = stored['events'][-2:]
            check_FE_rows(raw[1:], rendered)
        else:
            check_FE_rows(raw[1:], rendered)
            check_FE_rows(raw[1:]+b' '*parity, stored)
        records.append(receipt)
    assert len(records) == 17 and set(prefs['records']) == WIDTH_IDS
    save(OUT, dict(runtime=rt, initial_plan_sha256=digest(PLAN), records=records, no_ROM_written=True,
                   final_storage_checks_pending=True, new_credit=0))
    prefs['original_FE_probe'] = str(OUT)
    prefs['original_FE_probe_sha256'] = digest(OUT)
    save(PREFS, prefs)
    print('Bound two visible FE wrap findings and one pixel-identical Malacca parity case.')


if __name__ == '__main__':
    main()
