"""Distinguish owned terminal alignment-space events from actual glyph-row drift."""
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts import square_shopkeeper_font_oracles_v7020 as old_font
from scripts import Rafael_B45_FE_source_painter_v7894 as source_FE

ROOT = Path('work/analysis/Hodram_B171_B190_stored_FE_diagnostic_20261104')
REBUILT = Path('work/analysis/Hodram_B171_B190_rebuilt_20261104/reconstruction.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    rebuilt = load(REBUILT)
    native = load(rebuilt['native'])
    assert sha(Path(rebuilt['native']).read_bytes()) == rebuilt['native_sha256']
    ctx = RegisteredRuntime(native['runtime']['release_proof'], native['runtime']['startup_proof'])
    ascii_factory = FunctionType(old_font.make_painter.__code__, {**old_font.make_painter.__globals__, 'CURRENT_ARM9': sha(ctx.arm)}, argdefs=old_font.make_painter.__defaults__)
    factory = FunctionType(source_FE.make_source_painter.__code__, {**source_FE.make_source_painter.__globals__, 'CURRENT_ARM9': sha(ctx.arm), 'ASCII_painter': ascii_factory}, argdefs=source_FE.make_source_painter.__defaults__)
    painter, calibration = factory(ctx.image)
    by_id = {r['id']: r for r in native['records']}
    rows = []
    for group in rebuilt['groups']:
        for text in group['text_records']:
            raw = bytes.fromhex(text['stored_hex'])
            if raw[0] != 254 or not text['parity_space_added']:
                continue
            old = by_id[text['id']]
            baseline = bytes.fromhex(old['expanded_native_hex'])
            expanded = raw[1:].replace(b'FI', b'Hodram').replace(b'FA', b'Bergstrom').replace(b'FO', b'Bergstrom Fleet')
            assert expanded == baseline + b' '
            rendered = painter(expanded)
            target = [line.strip(b' ') for line in expanded.split(b'\n')]
            events = rendered['events']
            assert all(e['kind'] == 'ascii' for e in events)
            ys = sorted({e['y'] for e in events})
            actual = [bytes(e['code'] for e in events if e['y'] == y).strip(b' ') for y in ys]
            extra = [e for e in events if e['y'] not in range(0, 12 * len(target), 12)]
            path = Path(old['complete_native_English_display']['native_plane'])
            assert sha(path.read_bytes()) == old['complete_native_English_display']['native_plane_sha256']
            equal = rendered['physical'] == path.read_bytes()
            visible_rows_match = actual[:len(target)] == target and all(not r for r in actual[len(target):])
            rows.append(dict(id=text['id'], block=group['block'], stored_hex=raw.hex(), new_offset=text['new_offset'],
                source_alignment_flag=True, expanded_hex=expanded.hex(), original_expanded_hex=baseline.hex(),
                planned_rows=[r.decode('ascii') for r in target], actual_rows=[r.decode('ascii') for r in actual],
                actual_origins=ys, extra_events=extra, complete_plane_equal=equal, complete_visible_rows_match=visible_rows_match,
                native_events=events, native_plane_sha256=sha(rendered['physical'])))
    ROOT.mkdir()
    save(ROOT / 'diagnostic.json', dict(records=rows, runtime=ctx.receipt(), calibration=calibration,
        reconstruction=str(REBUILT), reconstruction_sha256=sha(REBUILT.read_bytes()),
        every_stored_FE_with_owned_terminal_alignment_space_checked=True, actual_gameplay=False,
        new_credit=0, producer_sha256=sha(Path(__file__).read_bytes())))
    for row in rows:
        if row['extra_events'] or not row['complete_visible_rows_match'] or not row['complete_plane_equal']:
            print({k: row[k] for k in ['id', 'planned_rows', 'actual_rows', 'extra_events', 'complete_plane_equal', 'complete_visible_rows_match']})
