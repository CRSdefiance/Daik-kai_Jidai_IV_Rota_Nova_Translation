"""Check the changed stored tail, all moved speech dispatches and original effect/end boundaries."""
from copy import deepcopy
from pathlib import Path
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.research_lil_B209_native_pages_v6461 import pages
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_stored_controls_v7840')
MAP=Path('work/analysis/retrospective_B218_relocation_v7839b/all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json')
FONT=Path('work/analysis/retrospective_B218_native_v7838/one_changed_wrap12_alignments_two_complete_current_native_planes.json')
INPUT=Path('work/analysis/current_V7821_Lil_native_v7837/current_native_input.json')
ADAPTER=Path('work/analysis/maria_confrontation_effective_v7790/all16_effective_English_templates32_original_dispatches.json')
CONTROL=Path('work/analysis/lil_B218_controls_v6878/two_A000_structural_cases50_normal_seeded_ends_no_relative_or_predicate.json')
OLD_STORED=Path('work/analysis/lil_B218_stored_v6895/all13_final_stored_targets52_alignments13_complete_pages.json')
START=Path('work/analysis/retrospective_Lil_context_binding_v7837/own_Lil_startup_andstrict_current_context.json')
if __name__=='__main__':
    assert not ROOT.exists()
    mapping,font,inp,control,oldstored,start=map(read,[MAP,FONT,INPUT,CONTROL,OLD_STORED,START])
    assert mapping['candidate_sha256']==font['candidate_sha256']==inp['current_ROM_sha256']
    g=mapping['groups'][0];block=Path(mapping['target_block']).read_bytes()
    assert sha(block)==g['target_block_sha256'] and (g['target_logical_end'],g['target_tail_bytes'])==(1018,2)
    target=next(r for r in g['text_records'] if r['id']=='DK4_MES_B218_R0027')
    old=next(r for r in oldstored['records'] if r['id']==target['id'])
    assert old['final_target_hex']==target['old_hex']
    compiled=bytes.fromhex(target['compiled_hex'])[1:];body=bytes.fromhex(target['target_hex'])[1:]
    assert body==compiled+b' ' and target['parity_space_added']
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    expansion=ctx.execute(expand,body,2);ctx.machines.pop()
    assert len(expansion['cases'])==4 and all(c['output_hex']==body.hex() for c in expansion['cases'])
    ns={**pages.__globals__,'expected_pixels':expected_pixels};exec(compile(font['source_owned_native_page_adapter'],__file__+'::exact-current-pages','exec'),ns)
    rendered=ns['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),body)
    base=next(p for p in font['native_planes'] if p['version']=='proposed-compiled')
    assert len(rendered['pages'])==len(base['pages'])==1
    for current,previous in zip(rendered['pages'],base['pages'],strict=True):
        pixels=bytes.fromhex(current.pop('native_plane_hex'))
        assert pixels==Path(previous['native_plane']).read_bytes() and sha(pixels)==previous['native_plane_sha256']
        file=ROOT/'changed_stored_complete_plane.bin';file.write_bytes(pixels)
        current.update(native_plane=str(file),native_plane_sha256=sha(pixels))
    unchanged=[]
    for r in g['text_records']:
        if r['id']==target['id']:continue
        previous=next(p for p in oldstored['records'] if p['id']==r['id'])
        assert r['old_hex']==r['target_hex']==previous['final_target_hex']
        unchanged.append(dict(id=r['id'],exact_previous_andcurrent_stored_hex=r['target_hex'],
            historical_stored_proof=str(OLD_STORED),not_represented_as_new_current_native_execution=True))
    assert len(unchanged)==12
    adapters=read(ADAPTER)['source_owned_dispatch_adapters']
    env={**inherited.__dict__,'SOURCE':INPUT,'route':2,'route_mask':4,'CATALOG_LOOKUP':{}}
    for name,text in adapters.items():exec(compile(text,__file__+'::'+name,'exec'),env)
    env['CATALOG_LOOKUP'],binding=env['bind_current_catalog'](ctx.rom)
    cases=[]
    for ref in g['text_records']:
        at=ref['new_offset'];raw=bytes.fromhex(ref['target_hex']);prefix=raw[0]
        assert block[at:at+len(raw)+1]==raw+b'\0' and block[at-5:at+1].hex()==ref['source_complete_preamble_hex']
        result=ctx.execute(env['dispatch'],prefix,raw[1:]);ctx.machines.pop()
        assert result['resolved_actor_ID']==prefix and result['source_voice_class']=={2:3,21:1}[prefix]
        assert result['registered_catalog_match'] is None
        boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body')
        assert boundary['text_hex']==raw[1:].hex()
        cases.append(dict(id=ref['id'],new_offset=at,target_hex=raw.hex(),**result))
    effect=next(c for c in g['all_target_commands'] if c['word']==0xA000)
    prior=next(c for c in control['source_A000_structural_cases'] if c['version']=='current')
    raw=block[effect['offset']:effect['offset']+effect['native_extent']]
    assert effect['native_extent']==8 and raw.hex()==prior['source_command_hex']=='00a0ffff2e000110'
    isolated=b'CS\0\1'+len(raw).to_bytes(2,'little')+bytes(2)+raw
    structural=walk(ctx.arm,isolated)
    assert structural['error'] is None and structural['rows']==prior['rows'] and structural['opaque_effect_bridges']==prior['opaque_effect_bridges']
    end=g['all_target_commands'][-1]['offset'];assert end==1014 and block[end:end+4]==bytes(4) and block[end+4:]==bytes(2)
    endenv=dict(end_case.__globals__);exec(compile(control['source_owned_seeded_end_adapter'],__file__+'::original-seeded-end','exec'),endenv)
    ends=[endenv['end_case'](ctx.arm,block,end,previous,seed) for previous in [0,1,2,3,0xFFFFFFFF] for seed in [0,1,2,3,0xFFFFFFFF]]
    assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
    assert not ctx.machines
    for sheet in [font['review_sheet'],start['review_sheet']]:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    save(ROOT/'one_changed_stored_plane13_dispatches_A00025_ends_andtwo_sheets_viewed.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],
        relocation_map=str(MAP),relocation_map_sha256=sha(MAP.read_bytes()),font_proof=str(FONT),font_proof_sha256=sha(FONT.read_bytes()),
        changed_stored_target=target,changed_stored_pipeline=expansion,changed_stored_pages=rendered,
        fresh_changed_stored_alignments=4,changed_parity_tail_zero_ink_complete_characters_bounds_andconsumption=True,
        other12_stored_bodies_exact=unchanged,historical_unchanged_stored_checks_not_relabelled_as_current=True,
        final_dispatch_cases=cases,all13_preambles_actor_voices_andzero_macro_bodies_bound=True,
        original_A000=prior,relocated_A000=structural,normal_terminal_seed_cases=ends,
        source_normal_end_type0_preserves_prior_value_in_all25_cases=True,
        two_zero_storage_tail_bytes_separate_from_complete_four_byte_terminal=True,
        opaque_A000_isolated_structural_bridge_not_full_effect_mechanics=True,
        offline_catalogue_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        own_Lil_startup_sheet_viewed=start['review_sheet'],before_after_native_sheet_viewed=font['review_sheet'],both_sheets_directly_viewed=True,
        actual_Lil_NewGame_frames=4001,actual_B218_scene_frames_added=0,
        reference_loader_caller_actual_policy_andregistered_release_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MAP,FONT,INPUT,ADAPTER,CONTROL,OLD_STORED,START,Path(__file__)]},
        full_goal_complete=False))
    print('Changed stored tail:4fresh alignments/complete plane exact;12stored bodies unchanged;13fresh dispatches/A000/25 normal carry ends pass.Both sheets viewed.Actual scene/release pending.')
