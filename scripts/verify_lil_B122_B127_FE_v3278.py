"""Ten FE records: complete native null-actor expansion, paper and pagination."""
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B122_B127_profile_v2 import profile_for
from dk4tool.dialogue.lil_B122_B127_layout_v1 import encode_relocatable_dialogue
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B122_B127_FE_v3278')
DOC = Path('translations/lil_B122_B127_editorial_manuscript_v3.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read(DOC)
    source = read(doc['source_context'])
    image = NdsImage.open(doc['current_ROM'])
    arm, common = image.read_file('/__arm9__.bin'), image.read_file('/COMMON/MESFILE.DK4')
    blocks = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    ROOT.mkdir(parents=True)
    contextpath = ROOT / 'historical_source_context.json'
    save(contextpath, dict(actual_snapshot=source['actual_historical_snapshot'],
        actual_snapshot_sha256=source['actual_historical_snapshot_sha256']))
    inputpath = ROOT / 'current_native_input.json'
    save(inputpath, dict(current_ROM=doc['current_ROM'], current_ROM_sha256=doc['current_ROM_sha256'],
        current_ARM9_sha256=sha(arm), current_COMMON_sha256=sha(common), native_context_proof=str(contextpath)))
    ctx = CurrentContext(inputpath, source['historical_snapshot_ROM'], ROOT / 'current_context')
    paint, calibration = make_painter(image)
    cases, pictures, staging = [], [], []
    calls = 0
    source_byid = {r['id']:r for r in source['records']}
    for row in doc['records']:
        if row['kind'] != 'system-FE':
            continue
        assert row['source_hex'] == source_byid[row['id']]['source_hex']
        profile = profile_for(arm, blocks[row['block']], 'FE-paper')
        encoded = encode_relocatable_dialogue(bytes.fromhex(row['source_hex']), row['english'], profile)
        assert encoded.encoded[:1] == b'\xfe' and encoded.encoded.hex() == row['compiled_hex']
        logical = row['english'].split('}',1)[1].replace('{MACRO:FI}','FI').replace('{MACRO:FA}','FA').replace('{MACRO:FO}','FO').encode('ascii')
        body = encoded.encoded[1:]
        sourcebody = bytes.fromhex(row['source_hex'])[1:]
        assert all(sourcebody.count(m) == body.count(m) for m in [b'FI', b'FA', b'FO'])
        expected=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        pipelines = []
        for kind, text in [('logical', logical), ('compiled-protected', body)]:
            pipelines.append(dict(kind=kind, **ctx.execute(expand, text)))
            calls += 4
            ctx.machines.pop()
        assert all(c['output_hex'] == expected.hex() for c in pipelines[1]['cases'])
        assert all(c['null_source_actor'] for pipeline in pipelines for c in pipeline['cases'])
        assert not body.startswith((b'\n', b' ')) and not logical.startswith((b'Sphinx:', b'Priest:', b'System:', b'Voice:'))
        target = paint(expected)
        assert target['complete_return_input_object_canaries_and_native_independent_plane_equal']
        visible = [e for e in target['events'] if e['code'] != 32]
        origins = {y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})}
        assert origins and all(x == 0 for x in origins.values())
        if sourcebody.startswith(b'\n'):
            assert min(origins) == 0
            staging.append(dict(id=row['id'], source_leading_LF_count=len(sourcebody)-len(sourcebody.lstrip(b'\n')),
                target_complete_first_line_safe=True, source_vertical_staging_not_reauthored_as_English_break=True))
        preview = ROOT / (row['id'] + '_complete_physical.png')
        picture = Image.new('RGB', (228,64))
        picture.putdata([(0,8,0) if v else (239,232,201) for v in target['physical']])
        picture.save(preview)
        pictures.append((row['id'],picture))
        plane = ROOT / (row['id'] + '_complete_logical_228x48.bin')
        plane.write_bytes(target['logical'])
        cases.append(dict(id=row['id'], encoded_hex=encoded.encoded.hex(), formatted_markup=encoded.formatted_markup,
            expanded_hex=expected.hex(), current_native_macro_pipelines=pipelines, native_glyphs=target['events'],
            one_native_page_consumes_complete_target=True, complete_native_independent_plane_and_all_glyphs_and_canaries_equal=True,
            all_visible_origins_zero_and4rows=True, visible_origins_by_row=origins,
            native_plane=str(plane), native_plane_sha256=sha(target['logical']),
            whole_physical228x64_plane_sha256=sha(target['physical']),
            preview=str(preview), preview_sha256=sha(preview.read_bytes()), object_rebindings=target['object_rebindings']))
    assert len(cases) == 10 and calls == 80 and len(staging) == 7 and not ctx.machines
    sheets = []
    for start in range(0,len(pictures),8):
        sheet = Image.new('RGB',(952,640),'#263238')
        draw = ImageDraw.Draw(sheet)
        for i,(ident,picture) in enumerate(pictures[start:start+8]):
            x,y = i%2*476,i//2*160
            draw.text((x+5,y+3),ident+' / FE paper',fill='white')
            sheet.paste(picture.resize((456,128),Image.Resampling.NEAREST),(x+5,y+24))
        path = ROOT / f'current_FE_sheet{start//8+1}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'current_FE_macro_font_and_typed_paper_proof.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,current_original_null_actor_macro_alignment_cases=calls,
        logical_geometry=[228,48],physical_geometry=[228,64],logical_rows_advance=12,physical_rows_advance=16,
        current_cold_typed_graphics_object_construction=True,no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter=True,
        all10_one_native_page_consumes_complete_target=True,all10_complete_native_independent_planes_all_glyphs_and_canaries_equal=True,
        all10_source_unlabeled_panels_preserved_without_invented_names_or_macros=True,source_FI_null_actor_cases=[r['id'] for r in doc['records'] if r['kind']=='system-FE' and b'FI' in bytes.fromhex(r['source_hex'])],
        source_leading_vertical_staging_cases=staging,seven_source_staging_cases_start_English_firstline_with_complete_glyphs=True,
        native_formatter_module='dk4tool/dialogue/lil_B122_B127_layout_v1.py',
        native_formatter_module_sha256=sha(Path('dk4tool/dialogue/lil_B122_B127_layout_v1.py').read_bytes()),
        historical_calibration=calibration,review_sheets=sheets,visual_review_pending=True,
        native_macro_context_plan=str(ctx.proof_path),native_macro_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        actual_selected_B122_B127_IDs=[],new_emulator_runs=0,reference_and_registered_release_pending=True,
        completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('10 complete FE planes,80 null-actor macro cases and7 original staging cases pass;two sheets require visual review. No gameplay or completion credit.')
