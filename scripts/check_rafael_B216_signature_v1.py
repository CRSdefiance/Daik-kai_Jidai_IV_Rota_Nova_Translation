"""Keep the B216 castle letter's original farewell and indented signature rows."""
from pathlib import Path

from PIL import Image, ImageDraw

from scripts.audit_story_glyph_consistency import load, save
from scripts.check_rafael_B166_staged_FE_v7 import actual_rows, candidates, native
from scripts.plan_rafael_B201_B220_v1 import ROOT, STAGED, STAGED_ID, digest
from scripts.probe_rafael_B166_FE_source_staging_v1 import build_painter
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


OUT = ROOT / 'staged_FE_native_v1'


def main():
    assert not OUT.exists()
    staged = load(STAGED)
    row, = staged['records']
    assert row['id'] == STAGED_ID and row['source_complete_preamble_hex'] == '0040ffff00fe'
    assert not row['native_literal_tokens']
    rt = staged['runtime']
    ctx = RegisteredRuntime(rt['release_proof'], rt['startup_proof'], captain=0)
    assert ctx.receipt() == rt
    painter, calibration = build_painter(rt)
    source, current = (bytes.fromhex(row[key]) for key in ('source_hex','current_hex'))
    assert source[0] == current[0] == 254
    clean_display, current_display = (painter(raw[1:]) for raw in (source,current))
    clean_rows, current_rows = (actual_rows(p['events']) for p in (clean_display,current_display))
    assert clean_display['complete_consumed_bytes'] == len(source)-1
    assert current_display['complete_consumed_bytes'] == len(current)-1
    assert len(clean_rows) == len(current_rows) == 2
    assert clean_rows[0] == (0,0,'じゃあ、元気でな')
    assert clean_rows[1] == (12,36,'ジャム・ジャック・ルドワイヤン')
    print('Letter rows (clean/current):', clean_rows, current_rows, flush=True)
    shape = [(clean_rows[i][1], row[k]) for i,k in enumerate(('localized_letter_farewell','localized_signature'))]
    assert ' '.join(t for _,t in shape) == row['english']
    expected = [(i*12,x,t) for i,(x,t) in enumerate(shape)]
    assert all(x+6*len(t) <= 228 for _,x,t in expected)
    adapter = checked_text(load(native.MACROS)['source_owned_FE_adapter'], {
        "b'Hodram'": "b'Rafael'", "b'Bergstrom'": "b'Castor'", "b'Bergstrom Fleet'": "b'Castor Co.'",
    })
    env = dict(native.FE_expand.__globals__)
    exec(compile(adapter, __file__+'::same-FE-expansion', 'exec'), env)
    for trial, body in enumerate(candidates(row, row['source_record_index'], shape), 1):
        display = painter(body)
        if actual_rows(display['events']) != expected:
            continue
        aligned = ctx.execute(env['expand'], body)
        if len(aligned['cases']) == 4 and all(case['output_hex'] == body.hex() for case in aligned['cases']):
            break
    else:
        raise AssertionError('The farewell and signature did not reach the original row origins.')
    assert b'\0' not in body and display['complete_consumed_bytes'] == len(body)
    OUT.mkdir()
    physical, logical = display.pop('physical'), display.pop('logical')
    binary = OUT / (STAGED_ID+'.bin')
    binary.write_bytes(physical)
    logical_file = OUT / (STAGED_ID+'_logical.bin')
    logical_file.write_bytes(logical)
    image = Image.new('RGB',(228,64))
    image.putdata([(0,8,0) if v else (239,232,201) for v in physical])
    image.save(binary.with_suffix('.png'))
    sheet = Image.new('RGB',(472,158),'#263238')
    ImageDraw.Draw(sheet).text((8,4),STAGED_ID+' | Castle letter farewell and signature',fill='white')
    sheet.paste(image.resize((456,128),Image.Resampling.NEAREST),(8,24))
    sheet_path = OUT/'FE_stage_sheet_1.png'
    sheet.save(sheet_path)
    proof = dict(id=STAGED_ID,source_reference=row['source_reference'],current_reference=row['current_reference'],
        logical_English=row['english'],source_complete_preamble_hex=row['source_complete_preamble_hex'],
        source_staging_reason='Preserve the source farewell row and the separate indented author signature.',
        clean_native_visible_rows=clean_rows,current_native_visible_rows=current_rows,
        encoded_hex=(b'\xfe'+body).hex(),expanded_hex=body.hex(),native_macro_alignments=aligned,
        planned_visible_rows=expected,complete_native_English_display=display,
        all_visible_row_origins_and_full_glyphs_exact=True,guard_candidates=trial,
        plane=str(binary),plane_sha256=digest(binary),logical_plane=str(logical_file),logical_plane_sha256=digest(logical_file))
    save(OUT/'staged_display.json',dict(runtime=rt,records=[proof],failed=[],
        review_sheets=[dict(path=str(sheet_path),sha256=digest(sheet_path),records=[STAGED_ID])],
        calibration=calibration,fresh_native_FE_ABI_alignments=4,stored_actual_and_direct_visual_review_pending=True,
        new_credit=0,evidence={str(p):digest(p) for p in (STAGED,Path(__file__))}))
    print('Two original letter row origins and four native FE alignments passed.', expected)


if __name__ == '__main__':
    main()

