"""Bind six exact stored dispatches and all nine final nontext commands to clean/current source."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_registered_route_context_v8303 import RouteCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_final_dispatch_v8328')
MAP=Path('work/analysis/Hodram_outcome_relocation_v8326/two_blocks6_speeches15_commands_full_source_parent_inverses.json')
STORED=Path('work/analysis/Hodram_outcome_stored_v8327/six_stored_bodies8_fresh16_reused_alignments_six_exact_native_pages.json')
SOURCE=Path('work/analysis/Hodram_B47_B48_source_display_v8316b/six_source_dispatches24_macro_alignments_five_progressive_one_FE_pages_Lil_identity_reuse.json')
INPUT=Path('work/analysis/current_V8300_Hodram_native_v8303/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,stored,source,inp=map(read,[MAP,STORED,SOURCE,INPUT]);assert stored['relocation_sha256']==sha(MAP.read_bytes()) and mapping['candidate_sha256']==inp['current_ROM_sha256']
    image=NdsImage.open(inp['current_ROM']);bank=IlnkContainer.parse(Path(mapping['target_archive']).read_bytes()).blocks
    ns={**inherited.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    for name,text in source['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    exec(compile(source['source_owned_macro_body_adapter'],__file__+'::same-captain1-defaults','exec'),ns);ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');dispatches=[];controls=[]
    for group in mapping['groups']:
        block=bank[group['block']];assert sha(block)==group['target_block_sha256']
        for ref in group['text_records']:
            raw=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];assert block[at:at+len(raw)+1]==raw+b'\0';is_FE=raw[0]==254
            result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
            boundary=next(b for b in result['boundaries'] if b['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'))
            expected=next(r for r in stored['records'] if r['id']==ref['id'])['expanded_stored_hex'];assert boundary['text_hex']==expected and result['resolved_actor_ID']==(None if is_FE else 2) and result['source_voice_class']==(None if is_FE else 3) and result['registered_catalog_match'] is None
            if is_FE:assert len(result['FE_original_null_actor_calls'])==1 and result['FE_original_null_actor_calls'][0]['args'][2]==0
            dispatches.append(dict(id=ref['id'],block=group['block'],final_offset=at,final_stored_hex=raw.hex(),**result))
        for a,b,c in zip(group['all_source_commands'],group['all_current_commands'],group['all_target_commands'],strict=True):
            assert a['word']==b['word']==c['word']
            if c['word']==0x4000:continue
            assert a['whole_command_hex']==b['whole_command_hex']==c['whole_command_hex']
            controls.append(dict(block=group['block'],source_offset=a['offset'],current_offset=b['offset'],target_offset=c['offset'],word=c['word'],complete_source_current_target_hex=c['whole_command_hex'],target_native_extent=c['native_extent']))
    assert len(dispatches)==6 and len(controls)==9 and not ctx.machines
    save(ROOT/'six_final_dispatches9_exact_nontext_commands_FE_FI_andcomplete_ends.json',dict(candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],relocation=str(MAP),relocation_sha256=sha(MAP.read_bytes()),final_dispatches=dispatches,nontext_commands=controls,registered_catalogue_binding=catalogue,
        all15_commands_six_preambles_source_FE_one_FI_nine_nonspeech_commands_full_ends_andtails_preserved=True,
        source_61FF_6302_6000_633D_623D_two_A000_bodies_exact=True,native_dispatch_UI_bodies_unexecuted_not_actual_geometry_orfull_effect_semantics=True,
        fifty_target_seeded_end_cases_bound_to_relocation=True,whole_original_scene_effect_semantics_actual_FE_geometry_palette_transition_andnormal_return_pending=True,
        source_owned_dispatch_adapters=source['source_owned_dispatch_adapters'],source_owned_macro_body_adapter=source['source_owned_macro_body_adapter'],new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [MAP,STORED,SOURCE,INPUT,Path(__file__)]}))
    print('Six final stored dispatches/one originalnullactorFE/one FI/nine exactnontextcommands/full4byte ends pass;actualeffects andtransitions pending.')
