"""Prove the three native heading rows and localized audience reactions."""
from pathlib import Path

from PIL import Image, ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_rafael_B166_staged_FE_v7 import actual_rows, candidates, wrap_options, native
from scripts.plan_rafael_B170_B176_display_v1 import ROOT, STAGED
from scripts.probe_rafael_B166_FE_source_staging_v1 import build_painter
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


OUT = ROOT / 'staged_FE_native_v1'


def main():
    assert not OUT.exists()
    manuscript = load(STAGED)
    rt = manuscript['runtime']
    ctx = RegisteredRuntime(rt['release_proof'], rt['startup_proof'], captain=0)
    assert ctx.receipt() == rt
    painter, calibration = build_painter(rt)
    env = dict(native.FE_expand.__globals__)
    adapter = checked_text(load(native.MACROS)['source_owned_FE_adapter'], {
        "b'Hodram'": "b'Rafael'", "b'Bergstrom'": "b'Castor'", "b'Bergstrom Fleet'": "b'Castor Co.'",
    })
    exec(compile(adapter, __file__+'::same-FE-expansion', 'exec'), env)
    OUT.mkdir()
    proofs = []
    sheet = Image.new('RGB', (920, 304), '#263238')
    pen = ImageDraw.Draw(sheet)
    for index, row in enumerate(manuscript['records']):
        ident = row['id']
        clean = bytes.fromhex(row['source_hex'])
        assert clean[0] == 254 and not row['native_literal_tokens']
        assert row['source_complete_preamble_hex'] == '0040ffff00fe'
        source = painter(clean[1:])
        source_rows = actual_rows(source['events'])
        assert len(source_rows) in (2,3) and source_rows[0] == (0,0,row['source_heading_row'])
        assert source['complete_consumed_bytes'] == len(clean)-1
        heading = ''.join(row['native_heading_tokens'])
        assert heading+' '+row['localized_modal_body'] == row['english']
        match = None
        for lines in wrap_options(row['localized_modal_body'], 3):
            shape = [(0, t) for t in (heading, *lines)]
            expected = [(i*12, 0, text) for i, (_, text) in enumerate(shape)]
            for raw in candidates(row, row['source_record_index'], shape):
                try:
                    display = painter(raw)
                    if actual_rows(display['events']) != expected:
                        continue
                    aligned = ctx.execute(env['expand'], raw)
                    assert len(aligned['cases']) == 4 and all(c['output_hex'] == raw.hex() for c in aligned['cases'])
                    match = raw, expected, display, aligned
                    break
                except AssertionError:
                    continue
            if match:
                break
        assert match, ident
        raw, expected, display, aligned = match
        assert b'\0' not in raw and display['complete_consumed_bytes'] == len(raw)
        assert all(x == 0 and y < 48 and len(t)*6 <= 228 for y,x,t in expected)
        physical, logical = display.pop('physical'), display.pop('logical')
        binary = OUT / (ident+'.bin')
        binary.write_bytes(physical)
        logical_file = OUT / (ident+'_logical.bin')
        logical_file.write_bytes(logical)
        image = Image.new('RGB',(228,64))
        image.putdata([(0,8,0) if v else (239,232,201) for v in physical])
        image.save(binary.with_suffix('.png'))
        x, y = (index%2)*460, (index//2)*152
        pen.text((x+4,y+3), ident, fill='white')
        sheet.paste(image.resize((456,128),Image.Resampling.NEAREST), (x,y+20))
        proofs.append(dict(id=ident, source_reference=row['source_reference'], current_reference=row['current_reference'],
            logical_English=row['english'], source_complete_preamble_hex=row['source_complete_preamble_hex'],
            clean_native_visible_rows=source_rows, exact_source_heading_row=True,
            encoded_hex=(b'\xfe'+raw).hex(), expanded_hex=raw.hex(), native_macro_alignments=aligned,
            planned_visible_rows=expected, complete_native_English_display=display,
            all_visible_row_origins_and_full_glyphs_exact=True, plane=str(binary), plane_sha256=sha(physical),
            logical_plane=str(logical_file), logical_plane_sha256=sha(logical)))
    assert len(proofs) == 3
    path = OUT/'FE_stage_sheet_1.png'
    sheet.save(path)
    save(OUT/'staged_display.json', dict(runtime=rt, records=proofs, failed=[],
        review_sheets=[dict(path=str(path),sha256=sha(path.read_bytes()),records=[p['id'] for p in proofs])],
        calibration=calibration, fresh_native_FE_ABI_alignments=12, stored_actual_and_direct_visual_review_pending=True,
        new_credit=0, evidence={str(p):sha(p.read_bytes()) for p in (STAGED, Path(__file__))}))
    print('Three original patron heading layouts and 12 native FE alignments passed.')


if __name__ == '__main__':
    main()
