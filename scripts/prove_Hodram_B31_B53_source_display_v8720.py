"""Complete clean B31/B53 source dispatch/pages and source-qualified branch paths."""
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B52_registered_route_context_v8707 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B31_B53_source_display_v8720')
GLOSS = Path('work/analysis/Hodram_B31_B53_clean_context_v8714/three_clean_glosses_explicit52_31_53_dependency_andunnamed_man_before_current_English.json')
CONTROL = Path('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json')
INPUT = Path('work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json')
NAMES = Path('work/analysis/Hodram_B31_actor34_names_v8719/source_names_native_getters_andplanes.json')
PRIOR_DISPLAY = Path('work/analysis/Hodram_B52_source_display_v8626/source_display.json')
FORWARD = Path('work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    gloss, control, inp, names, prior, forward = map(read, [GLOSS, CONTROL, INPUT, NAMES, PRIOR_DISPLAY, FORWARD])
    assert gloss['current_English_for_B31_andB53_still_unconsulted'] and names['current_B31_B53_English_dialogue_bodies_unconsulted']
    image = NdsImage.open(inp['current_ROM']); clean = NdsImage.open('work/clean.nds')
    arm, font = image.read_file('/__arm9__.bin'), image.read_file('/GRP/KANJI.FNT')
    assert sha(Path(inp['current_ROM']).read_bytes()) == inp['current_ROM_sha256'] == names['candidate_sha256'] == control['candidate_sha256']
    assert sha(arm) == prior['ARM9_sha256'] and sha(font) == prior['font_sha256']
    assert image.read_file('/COMMON/MESFILE.DK4') == NdsImage.open(prior['candidate']).read_file('/COMMON/MESFILE.DK4')
    ns = {**inherited.__dict__, 'SOURCE': INPUT, 'route': 1, 'route_mask': 2, 'CATALOG_LOOKUP': {}}
    adapters = prior['source_owned_dispatch_adapters']
    for key, text in adapters.items():
        exec(compile(text, __file__+'::'+key, 'exec'), ns)
    ns['CATALOG_LOOKUP'], catalogue = ns['bind_current_catalog'](image)
    exec(compile(prior['source_owned_macro_body_adapter'], __file__+'::current-captain1-substitutions', 'exec'), ns)
    pe = dict(progressive_expand.__globals__)
    exec(compile(prior['source_owned_progressive_adapter'], __file__+'::source-captain1-progressive', 'exec'), pe)
    pixels, unused_factory, oracle = bind(image)
    page_env = {**original_pages.__globals__, 'expected_pixels': pixels, 'codes': codes}
    exec(compile(prior['source_owned_target_page_adapter'], __file__+'::complete-source-pages', 'exec'), page_env)
    voices = {r['source_selector']:r['original_voice_class'] for r in names['fresh_actor34_source_voice']['rows']+names['scoped_reused_actor113']['source_voice']}
    assert set(voices) == {34,113}
    ROOT.mkdir(parents=True); ctx = RouteCurrentContext(INPUT, 'unused-no-historical-ROM', ROOT/'current_context')
    rows = []; pictures = []
    for group in gloss['groups']:
        for row in group['records']:
            raw = bytes.fromhex(row['source_hex']); prefix, body = raw[0],raw[1:]
            assert prefix in voices and body not in ns['CATALOG_LOOKUP']
            assert row['source_complete_preamble_hex'] == '0040ffff00'+bytes([prefix]).hex()
            result = ctx.execute(ns['dispatch'], prefix, body); ctx.machines.pop()
            assert result['resolved_actor_ID'] == prefix and result['source_voice_class'] == voices[prefix]
            boundary = next(b for b in result['boundaries'] if b['kind'] == 'unexecuted-progressive-body')
            assert boundary['text_hex'] == body.hex() and result['registered_catalog_match'] is None and not result['FE_original_null_actor_calls']
            aligned = ctx.execute(pe['expand'], body, prefix); ctx.machines.pop()
            assert len(aligned['cases']) == 4 and all(c['output_hex'] == body.hex() for c in aligned['cases'])
            rendered = page_env['pages'](arm, font, body)
            assert rendered['complete_consumed_bytes'] == len(body)
            for page in rendered['pages']:
                plane = bytes.fromhex(page.pop('native_plane_hex')); path = ROOT/(row['id']+f'_page{page["page"]}.bin'); path.write_bytes(plane)
                page.update(native_plane=str(path), native_plane_sha256=sha(plane))
                picture = Image.new('RGB',(216,64)); colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
                picture.putdata([colors[v] for v in plane]); pictures.append((row['id']+f' clean p{page["page"]}',picture))
            rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_reference=row['source_reference'],
                source_selector=prefix,source_hex=raw.hex(),complete_source_preamble_hex=row['source_complete_preamble_hex'],
                source_0100_ancestors=row['source_0100_ancestors'],original_dispatch=result,original_four_alignments=aligned,complete_native_source_display=rendered))
    assert len(rows) == 3 and sum(len(r['original_four_alignments']['cases']) for r in rows) == 12 and not ctx.machines
    # Reuse the complete unchanged caller's measured kind2 forwarding/kind3 carry
    # contract. The query is NOT replaced or forced to obtain an alternate path.
    caller_start, caller_end = 0x24048,0x24118
    assert arm[caller_start:caller_end] == clean.read_file('/__arm9__.bin')[caller_start:caller_end]
    assert forward['original_caller_span']['sha256'] == sha(arm[caller_start:caller_end]) and len(forward['caller_fragment_cases']) == 50
    assert all(c['all_six_return_words_preserved'] and c['next_parser_r3'] == (c['result'][1] if c['result'][0] == 2 else c['previous_structural_value']) for c in forward['caller_fragment_cases'])
    b31 = next(g for g in control['groups'] if g['block'] == 31); commands={c['offset']:c for c in b31['all_original_source_commands']}; branches={c['offset']:c for c in b31['source_relative_cases']}
    paths=[]
    for previous in [0,1]:
        at=18; visited=[8,10]; speeches=[]
        while True:
            visited.append(at); command=commands[at]
            if command['word'] == 0: break
            if at in branches:
                at=next(c['next_offset'] for c in branches[at]['cases'] if c['previous_result_structural_argument'] == previous)
            else:
                if command['word'] == 0x4000: speeches.append(at)
                at += command['native_extent']
            assert len(visited)<15
        assert (speeches,at) == ([26] if previous == 0 else [90],192)
        paths.append(dict(query_value_structural_argument=previous,source_command_offsets=visited,source_speech_headers=speeches,source_terminal_offset=at,
            structural_composition_not_forced_native_predicate_oractual_activation=True,not_two_consecutive_speeches=True))
    native_query=b31['source_raw_query_cases'][0]
    assert native_query['native_result'] == [2,1,0,0,0,0]
    count=len(pictures)
    for name in names['fresh_actor34_name_planes']:
        pictures.append((name['text']+' (fresh name plane)',Image.open(name['preview']).convert('RGB')))
    reused=names['scoped_reused_actor113']['plane']; pictures.append(('Port Worker (exact reused name)',Image.open(reused['preview']).convert('RGB')))
    sheet=Image.new('RGB',(912,((len(pictures)+1)//2)*160),'#263238'); draw=ImageDraw.Draw(sheet)
    for n,(text,picture) in enumerate(pictures):
        x,y=n%2*456,n//2*160;draw.text((x+3,y+3),text+' offline native',fill='white');sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
    sheetfile=ROOT/'complete_clean_source_pages_andbound_names.png';sheet.save(sheetfile)
    save(ROOT/'source_display_andbranch_paths.json',dict(candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),source_controls=str(CONTROL),source_controls_sha256=sha(CONTROL.read_bytes()),
        source_names=str(NAMES),source_names_sha256=sha(NAMES.read_bytes()),records=rows,complete_native_source_page_count=count,
        original_B31_structural_paths=paths,original_unforced_B31_query_result=native_query,
        original_query_value1_inown_opening_native_context_composes_long_variant_not_actual_B31_activation=True,
        raw_query_operand_not_named_plot_predicate_nor_assumed_boolean_forall_states=True,
        original_caller_code=forward['original_caller_span'],reused_fifty_caller_fragment_cases=str(FORWARD),reused_fifty_caller_fragment_cases_sha256=sha(FORWARD.read_bytes()),
        source_owned_dispatch_adapters=adapters,source_owned_macro_body_adapter=prior['source_owned_macro_body_adapter'],
        source_owned_progressive_adapter=prior['source_owned_progressive_adapter'],source_owned_target_page_adapter=prior['source_owned_target_page_adapter'],
        target_oracle_binding=oracle,registered_catalogue_binding=catalogue,source_macro_counts=dict(FI=0,FA=0,FO=0),source_FE_count=0,
        review_sheet=dict(path=str(sheetfile),sha256=sha(sheetfile.read_bytes())),direct_view_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        current_B31_B53_English_bodies_still_unconsulted=True,full_name_middle_field_decision_andactual_scene_headers_pending=True,
        no_gameplay_original_location_chronology_earned_flags_custom_names_orfull_catalogue_UI_claim=True,
        no_ROM_registry_orcompletion_credit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,CONTROL,INPUT,NAMES,PRIOR_DISPLAY,FORWARD,Path(__file__)]}))
    print(f'Three clean source dispatches/12 guarded alignments/{count} complete pages pass. B31 variants are separate paths; query unforced. Current English unread.',flush=True)
