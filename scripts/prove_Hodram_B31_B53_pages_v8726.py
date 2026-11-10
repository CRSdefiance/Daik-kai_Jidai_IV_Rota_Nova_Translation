"""Three complete B31/B53 native English speech pages and twelve compiled macro alignments; no typed choices."""
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B52_registered_route_context_v8707 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B31_B53_pages_v8726')
DOC = Path('translations/hodram_B31_B53_editorial_manuscript_v1.json')
PLAN = Path('work/analysis/Hodram_B31_B53_layout_v8725/automatic_plans.json')
LOGICAL = Path('work/analysis/Hodram_B31_B53_logical_v8724/logical_paragraphs.json')
SOURCE = Path('work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json')
INPUT = Path('work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc, plan, logical, source = map(read, [DOC, PLAN, LOGICAL, SOURCE])
    assert plan['manuscript_sha256'] == logical['manuscript_sha256'] == sha(DOC.read_bytes()) and not plan['failures'] and len(plan['records']) == 3
    assert not any(i['severity'] in ['warning', 'error'] for r in plan['records'] for i in r['base_QA']['issues'])
    image = NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256']
    arm, font = image.read_file('/__arm9__.bin'), image.read_file('/GRP/KANJI.FNT')
    pixels, unused_factory, oracle = bind(image)
    pe = {**original_pages.__globals__, 'expected_pixels': pixels, 'codes': codes}
    page_adapter = source['source_owned_target_page_adapter']
    exec(compile(page_adapter, __file__ + '::unchanged-current-complete-pages', 'exec'), pe)
    prog = dict(progressive_expand.__globals__)
    exec(compile(logical['source_owned_progressive_adapter'], __file__ + '::unchanged-progressive-wrapper', 'exec'), prog)
    ROOT.mkdir(parents=True)
    ctx = RouteCurrentContext(INPUT, 'unused-no-historical-ROM', ROOT / 'current_context')
    rows, pictures = [], []
    for row, p in zip(doc['records'], plan['records'], strict=True):
        assert row['id'] == p['id']
        raw = bytes.fromhex(p['encoded_hex'])
        prefix, body = raw[0], raw[1:]
        assert prefix == row['source_selector'] and body and not any(v in body for v in [b'\0', b'%'])
        assert not body.startswith((b' ', b'\n')) and not body.endswith((b' ', b'\n'))
        aligned = ctx.execute(prog['expand'], body, prefix)
        ctx.machines.pop()
        assert len(aligned['cases']) == 4 and all(c['output_hex'] == body.hex() for c in aligned['cases'])
        assert ' '.join(body.decode('cp932').split()) == row['english']
        rendered = pe['pages'](arm, font, body)
        for page in rendered['pages']:
            plane = bytes.fromhex(page.pop('native_plane_hex'))
            file = ROOT / (row['id'] + f'_page{page["page"]}.bin')
            file.write_bytes(plane)
            segment = body[page['start']:page['end']]
            assert not segment.startswith(b' ') and page['first_visible_origin'] == [0, 0]
            picture = Image.new('RGB', (216, 64))
            colors = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}
            picture.putdata([colors[v] for v in plane])
            preview = file.with_suffix('.png')
            picture.save(preview)
            page.update(native_plane=str(file), native_plane_sha256=sha(plane), preview=str(preview), preview_sha256=sha(preview.read_bytes()),
                complete_first_internal_final_codes_bounds_consumption_andindependent_ink_exact=True)
            pictures.append((row['id'] + f' p{page["page"]}', picture))
        assert rendered['complete_consumed_bytes'] == len(body) and len(rendered['pages']) == p['expected_native_pages'] == 1
        rows.append(dict(id=row['id'], file_path=row['file_path'], block=row['block'], source_record_index=row['source_record_index'],
            source_selector=prefix, kind=row['kind'], source_reference=row['source_reference'], current_reference=row['current_reference'],
            compiled_hex=raw.hex(), expanded_native_hex=body.hex(), logical_English=row['english'], formatted_markup=p['formatted_markup'], native_alignment=aligned, **rendered))
    assert len(rows) == len(pictures) == 3 and not ctx.machines
    sheet = Image.new('RGB', (912, 320), '#263238')
    draw = ImageDraw.Draw(sheet)
    for index, (label, picture) in enumerate(pictures):
        x, y = index % 2 * 456, index // 2 * 160
        draw.text((x + 3, y + 3), label + ' offline native', fill='white')
        sheet.paste(picture.resize((432, 128), Image.Resampling.NEAREST), (x, y + 24))
    path = ROOT / 'three_complete_English_native_pages.png'
    sheet.save(path)
    save(ROOT / 'compiled_native_pages.json', dict(candidate=doc['current_ROM'], candidate_sha256=doc['current_ROM_sha256'], ARM9_sha256=sha(arm), font_sha256=sha(font),
        manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), plan=str(PLAN), plan_sha256=sha(PLAN.read_bytes()), records=rows,
        fresh_compiled_alignment_cases=12, progressive_alignment_cases=12, FE_null_actor_alignment_cases=0, complete_progressive_pages=3,
        all_complete_leading_internal_final_characters_native_independent_planes_bounds_andconsumption_exact=True,
        all_three_speech_single_pages_no_blank_orunintended_extra_page=True, zero_source_macros_preserved_no_shortening_orprose_manual_wrap=True,
        target_oracle_binding=oracle, source_owned_target_page_adapter=page_adapter, source_owned_progressive_adapter=logical['source_owned_progressive_adapter'],
        review_sheet=dict(path=str(path), sha256=sha(path.read_bytes())), direct_view_pending=True, all_three_formatting_gates_still_false=True,
        stored_controls_actual_branch_context_headers_transitions_policy_andregistered_release_pending=True,
        new_credit=0, new_emulator_runs=0, full_goal_complete=False, native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p): sha(p.read_bytes()) for p in [DOC, PLAN, LOGICAL, SOURCE, INPUT, Path('scripts/Hodram_FE_font_oracles_v8315.py'), Path(__file__)]}))
    print('Three complete native B31/B53 English speech pages, twelve compiled alignments, complete glyphs/bounds/consumption. Direct view, stored controls, actual and registered release pending.')
