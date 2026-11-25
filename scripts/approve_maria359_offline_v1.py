"""Seal the directly viewed final Maria359 pages, retaining all native and compound guards."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B253_B274_clean_20261110')


def main():
    out = ROOT/'offline_display_approval_v1.json'
    assert not out.exists()
    paths = {k: ROOT/v for k,v in dict(
        manuscript='formatting_v1/formatting_input_v2.json', plan='plan_v7/automatic_plans.json',
        joined='compiled_final_v2/compiled_native_pages.json', baseline='native_body_v1/compiled_native_pages.json',
        styles='compiled_styles_v2/compiled_style_objects.json', menu='menu_native_v1/group_verification.json',
        names='name_planes_v1/native_name_planes.json', mixed='mixed_visual_review_v1.json',
        macros='formatting_v1/native_macro_measurements.json', objects='current_objects_v1/current_objects.json').items()}
    d = {k: load(p) for k,p in paths.items()}
    doc,plan,native = d['manuscript'],d['plan'],d['joined']
    assert len(doc['records']) == 359 and doc['complete_exchanges'] == 22
    assert Counter(r['decision'] for r in doc['records']) == {'revision':219,'retention':140}
    assert all(r['review'] == dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert plan['manuscript_sha256'] == native['manuscript_sha256'] == digest(paths['manuscript'])
    assert native['plan_sha256'] == digest(paths['plan']) and not plan['failures']
    assert not any(i['severity'] in ['error','warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert all(d[k]['runtime'] == doc['runtime'] for k in ['joined','baseline','styles','menu','names','macros','objects'])
    originals = {r['id']:r for r in doc['records'] if r['kind'] != 'typed-choice-label'}
    plans = {r['id']:r for r in plan['records']}
    assert originals.keys() == plans.keys() == {r['id'] for r in native['records']}
    runs = {}; receipts = {}; allplanes = set()
    for row in native['records']:
        key = row['id']; source = originals[key]; origin = native['origins'][key]
        assert digest(origin['proof']) == origin['proof_sha256']
        receipt = Path(origin['proof']).parent/('complete_'+key+'.json')
        proof = load(receipt)
        assert proof['record'] == row and proof['four_native_alignment_cases_pass']
        assert proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
        assert row['compiled_hex'] == plans[key]['encoded_hex'] and row['logical_English'] == source['english']
        assert all(row[k] == source[k] for k in ['source_reference','current_reference'])
        assert len(row['native_alignment']['cases']) == 4
        runpath = proof['native_run_inputs']; assert digest(runpath) == proof['native_run_inputs_sha256']
        if runpath not in runs:
            run = load(runpath); runs[runpath] = run
            assert run['runtime'] == doc['runtime'] and run['font_sha256'] == native['font_sha256']
            assert run['all_v1_native_assertions_preserved'] and run['macro_proof_sha256'] == digest(paths['macros'])
            for field in ['source_owned_target_page_adapter','source_owned_progressive_macro_adapter']:
                assert run[field] == d['baseline'][field]
        receipts[key] = dict(path=str(receipt),sha256=digest(receipt))
        display = row['complete_native_English_display']
        pages = display['pages'] if row['kind'] == 'progressive' else [display]
        assert len(pages) == plans[key]['expected_native_pages']
        if row['kind'] == 'progressive':
            assert display['all_visible_first_internal_final_characters_in_order'] and display['no_blank_or_overlap_page']
            assert display['complete_consumed_bytes'] == len(bytes.fromhex(row['expanded_native_hex']))
            assert all(p['native_independent_plane_equal'] and p['all_bitmap_header_input_canaries_exact'] for p in pages)
        else:
            assert display['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            assert display['input_bitmap_header_view_context_canaries_andcomplete_return_exact']
            assert display['all_executed_instructions_exact_current_sections_andpayload']
            assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
        for number,page in enumerate(pages,1):
            assert digest(page['native_plane']) == page['native_plane_sha256'] and digest(page['preview']) == page['preview_sha256']
            allplanes.add((key,number,page['native_plane_sha256']))
    assert len(originals) == 349 and len(allplanes) == native['pages'] == 350
    # All thirty final-v6 sheets, the superseded seven-page sheet and the new cure sheet were read.
    # Retain alternative page planes as triples; superseded versions never overwrite current pages.
    viewed = {}; sheets = []
    for name in ['body_sheets_final_v1','body_sheets_superseded_v1']:
        manifestpath = ROOT/name/'contact_sheet_manifest.json'; manifest = load(manifestpath)
        assert digest(manifest['receipt']) == manifest['receipt_sha256']
        for sheet in manifest['review_sheets']:
            assert digest(sheet['path']) == sheet['sha256']
            with Image.open(sheet['path']) as canvas:
                canvas = canvas.convert('RGB')
                for i,member in enumerate(sheet['members']):
                    assert digest(member['preview']) == member['preview_sha256']
                    with Image.open(member['preview']) as image:
                        image = image.convert('RGB'); scaled = image.resize((image.width*2,image.height*2),Image.Resampling.NEAREST)
                    x,y = i%2*456,i//2*160+24
                    assert canvas.crop((x,y,x+scaled.width,y+scaled.height)).tobytes() == scaled.tobytes()
                    viewed[(member['id'],member['page'],member['native_plane_sha256'])] = dict(member,viewed_sheet=sheet['path'],viewed_sheet_sha256=sheet['sha256'],exact_viewed_pixels_equal=True)
            sheets.append(dict(sheet,directly_viewed=True))
        paths[name] = manifestpath
    curepath = ROOT/'native_cure_v1/compiled_native_pages.json'; cure = load(curepath)
    assert len(cure['records']) == cure['pages'] == 1
    row = cure['records'][0]; page = row['complete_native_English_display']['pages'][0]; sheet = cure['review_sheets'][0]
    assert digest(sheet['path']) == sheet['sha256']
    with Image.open(sheet['path']) as canvas, Image.open(page['preview']) as image:
        image = image.convert('RGB'); scaled = image.resize((image.width*2,image.height*2),Image.Resampling.NEAREST)
        assert canvas.convert('RGB').crop((0,24,scaled.width,24+scaled.height)).tobytes() == scaled.tobytes()
    viewed[(row['id'],1,page['native_plane_sha256'])] = dict(page,page=1,viewed_sheet=sheet['path'],viewed_sheet_sha256=sheet['sha256'],exact_viewed_pixels_equal=True)
    sheets.append(dict(sheet,directly_viewed=True)); paths['cure'] = curepath
    assert allplanes <= viewed.keys() and len(viewed) == 359 and len(sheets) == 32
    raw = [ROOT/'native_body_v1'/f'DK4_MES_B272_R{n:04d}_p1.png' for n in [114,118]]
    names,menu,styles,objects = [d[k] for k in ['names','menu','styles','objects']]
    assert d['mixed']['all_name_andcaption_sheets_directly_viewed']
    assert d['mixed']['names_sha256'] == digest(paths['names']) and d['mixed']['menus_sha256'] == digest(paths['menu'])
    assert names['actors'] == 18 and len(names['planes']) == names['distinct_current_strings'] == 21
    cursor = 0
    for sheet in names['review_sheets']:
        assert digest(sheet['path']) == sheet['sha256']
        part = names['planes'][cursor:cursor+sheet['strings']]
        with Image.open(sheet['path']) as canvas:
            for i,plane in enumerate(part):
                assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
                assert digest(plane['native_plane']) == plane['native_plane_sha256'] and digest(plane['preview']) == plane['preview_sha256']
                with Image.open(plane['preview']) as image:
                    expected = image.convert('RGB').crop((0,0,216,16)).resize((432,32),Image.Resampling.NEAREST)
                x,y = i%2*456,i//2*64+22
                assert canvas.convert('RGB').crop((x,y,x+432,y+32)).tobytes() == expected.tobytes()
        cursor += len(part)
    assert cursor == 21
    choices = {(r['block'],r['source_command_offset'],r['source_index']):r for r in doc['records'] if r['kind']=='typed-choice-label'}
    for item in menu['objects']:
        assert digest(item['proof']) == item['proof_sha256']; proof = load(item['proof'])
        assert proof['runtime'] == doc['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        for plane in proof['records']: assert digest(plane['path']) == plane['sha256']
        rows = [choices[(item['block'],item['source_command_offset'],i)] for i in range(item['caption_count'])]
        assert [r['id'] for r in rows] == item['record_ids']
        assert compile_choices(bytes.fromhex(item['source_object_hex']),bytes.fromhex(item['current_object_hex']),rows,require_formatting=False).hex() == item['target_object_hex']
        for sheet in item['review_sheets']: assert digest(sheet['path']) == sheet['sha256']
    assert menu['menus'] == 5 and menu['captions'] == len(choices) == 10
    stylerows = [r for r in doc['records'] if r.get('native_object_kind') == '4100-style-alternative']
    assert len(stylerows) == styles['physical_alternatives'] == len(objects['style_records']) == 131
    assert len(styles['objects']) == len(objects['style_objects']) == 18 and styles['native_target_slot_cases'] == 144
    assert styles['manuscript_sha256'] == digest(paths['manuscript']) and styles['plan_sha256'] == digest(paths['plan'])
    for item in styles['objects']:
        rows = sorted([r for r in stylerows if r['block']==item['block'] and r['source_command_offset']==item['source_command_offset']],key=lambda r:r['source_reference']['offset'])
        assert [r['id'] for r in rows] == item['physical_record_IDs']
        assert compile_styles(bytes.fromhex(item['source_object_hex']),bytes.fromhex(item['current_object_hex']),rows,plans,require_formatting=False).hex() == item['target_object_hex']
        assert digest(item['target_path']) == item['target_sha256']
        assert all(bytes.fromhex(plans[s['record_id']]['encoded_hex'])[1:].hex() == s['target_hex'] for s in item['native_slots'])
    assert sum(len(n['rejected']) for n in styles['compiler_negatives']) == 162
    bodypath,finalpath,menupath = [ROOT/p for p in ['body_visual_review_v1.json','final_native_v2.json','menu_native_approved_v1.json']]
    assert not any(p.exists() for p in [bodypath,finalpath,menupath])
    save(bodypath,dict(records=[dict(id=r['id'],compiled_hex=r['compiled_hex'],pages=[viewed[(r['id'],i,p['native_plane_sha256'])] for i,p in enumerate(r['complete_native_English_display']['pages'] if r['kind']=='progressive' else [r['complete_native_English_display']],1)]) for r in native['records']],
        body_records=349,body_pages=350,generated_pages_directly_viewed=359,superseded_pages_directly_viewed=9,review_sheets=sheets,
        individual_raw_checks={str(p):digest(p) for p in raw},runtime=doc['runtime'],all_final_body_pages_bound_to_directly_viewed_exact_native_pixels=True,
        selected_plan=str(paths['plan']),selected_plan_sha256=digest(paths['plan']),actual_gameplay=False,new_credit=0))
    final = deepcopy(d['baseline']); final.update(native)
    final.update(selected_alignment_cases=1396,fresh_native_records=8,exact_unchanged_native_records_reused=341,
        selected_native_receipt_per_record=receipts,direct_visual_review_pending=False,review_sheets=sheets,
        all_final_pages_directly_viewed_or_exact_visual_dependency_reuse=True,formatting_gates_still_false=True)
    save(finalpath,final)
    save(menupath,dict(runtime=doc['runtime'],manuscript=str(paths['manuscript']),manuscript_sha256=digest(paths['manuscript']),menus=menu['objects'],
        source_index_andcount_preserved=True,offline_visual_approved=True,direct_view_pending=False,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,original_receipt=str(paths['menu']),original_receipt_sha256=digest(paths['menu']),actual_gameplay=False,new_credit=0))
    evidence = {str(p):digest(p) for p in [*paths.values(),bodypath,finalpath,menupath,Path(__file__)]}
    save(out,dict(source_objects=359,complete_exchanges=22,dialogue_revisions=219,dialogue_retentions=140,
        physical_body_candidates=349,body_pages=350,selected_alignment_cases=1396,all_final_body_pages_directly_viewed=True,
        source_styles=131,source_style_objects=18,style_slot_cases=144,style_compiler_negatives=162,
        choice_menus=5,choice_captions=10,scoped_names=18,distinct_name_strings=21,fresh_name_planes=4,reused_name_planes=17,names_sha256=digest(paths['names']),
        all_names_andcaptions_directly_viewed=True,menu_native_provider_alignments=30,menu_bridged_returns=90,
        menu_normal_highlight_planes=40,target_menu_normal_highlight_planes=20,menu_compiler_negatives=35,
        final_native_proof=str(finalpath),final_native_proof_sha256=digest(finalpath),all_native_controls_substitutions_words_glyphs_bounds_andpagination_pass=True,
        stored_script_allocation_branches_actual_gameplay_andregistration_pending=True,all_fifth_formatting_gates_still_pending=True,
        actual_gameplay=False,new_ROM=False,new_credit=0,full_goal_complete=False,evidence=evidence))
    print('Maria359 offline approval:349 bodies/350 pages,359 generated pages viewed,18 names/21 strings,10 captions. Storage/gameplay/release remain.')


if __name__ == '__main__': main()
