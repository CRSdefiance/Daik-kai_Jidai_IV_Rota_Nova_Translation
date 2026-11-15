"""Independently execute stored dispatches/EV1 entries/normal ends and bind original opaque controls."""
import struct
from pathlib import Path
from tempfile import TemporaryDirectory
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_outcomes_profile_v6 import contract
from dk4tool.patch.hodram_outcomes_native_guards_v6 import trusted_adapter,CONTROLS
from dk4tool.patch.hodram_outcomes_loaders_v1 import check_loaders_and_census as original_loaders
from scripts.Hodram_registered_route_context_v8303 import RouteCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read

INPUT=Path('work/analysis/current_V8300_Hodram_native_v8303/current_native_input.json')

def check_controls(data,rows,parent,reference,rebuilt,native,load,require):
    source=data['source_controls'];controls=data['controls'];display=data['source_display'];arm=parent.read_file('/__arm9__.bin');cleanarm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    require(arm==reference.read_file('/__arm9__.bin') and sha(arm)=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b','exact registered name/runtime dependency for controls')
    dispatch=trusted_adapter('dispatch',display['source_owned_dispatch_adapters']);macro=trusted_adapter('macro_body',display['source_owned_macro_body_adapter'])
    require(controls['source_owned_dispatch_adapters']==dispatch and controls['source_owned_macro_body_adapter']==macro,'exact final dispatch adapters')
    ns={**dispatch_base.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    for name,text in dispatch.items():exec(compile(text,__file__+'::trusted-'+name,'exec'),ns)
    exec(compile(macro,__file__+'::trusted-macro','exec'),ns);ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](parent)
    require(catalogue==controls['registered_catalogue_binding'] and len(catalogue['records'])==467,'complete original catalogue binding')
    require(len(controls['final_dispatches'])==6 and {d['id'] for d in controls['final_dispatches']}=={r['id'] for r in rows},'six unique final dispatch identities')
    rawsource=CONTROLS.read_bytes();require(contract()['dependencies'].get(str(CONTROLS.resolve()))==sha(rawsource),'trusted original source controls artifact')
    original=load(CONTROLS);entryadapter=original['source_owned_EV1_entry_adapter'];require(source['source_owned_EV1_entry_adapter']==entryadapter,'trusted original EV1 entry adapter')
    en=dict(native_entry.__globals__);exec(compile(entryadapter,__file__+'::trusted-entry','exec'),en)
    endadapter=trusted_adapter('seeded_end',source['source_owned_seeded_end_adapter']);ends=dict(end_case.__globals__);exec(compile(endadapter,__file__+'::trusted-end','exec'),ends)
    events=source['source_event_records'];require([(e['event_ID'],e['action_index'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in events]==[(47,48,47,[],[48]),(48,49,48,[],[])],'two original EV1 outcomes and asymmetric exclusions')
    require(source['source_relative_sites']==source['source_raw_predicates']==0 and source['normal_seeded_end_cases']==50,'source absence of relatives/queries andcomplete end count')
    expected_controls=[];endcount=0;opaque=0
    with TemporaryDirectory(prefix='Hodram-outcomes-controls-') as temporary:
        ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',Path(temporary)/'native-context')
        entry=ctx.execute(en['native_entry'],parent.read_file('/data/EV1.DK4'),events);ctx.machines.pop();require(entry==source['original_EV1_entry'],'independent original EV1 getters match all recorded entries')
        for d in controls['final_dispatches']:
            group=next(g for g in rebuilt['groups'] if g['block']==d['block']);ref=next(r for r in group['text_records'] if r['id']==d['id']);raw=bytes.fromhex(ref['target_hex']);is_FE=raw[0]==254
            require(d['final_offset']==ref['new_offset'] and d['final_stored_hex']==raw.hex(),'final stored dispatch offset/body')
            fresh=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
            require(d==dict(id=ref['id'],block=group['block'],final_offset=ref['new_offset'],final_stored_hex=raw.hex(),**fresh),'independent full final dispatch fields andABI guards')
            require(fresh['resolved_actor_ID']==(None if is_FE else 2) and fresh['source_voice_class']==(None if is_FE else 3) and fresh['registered_catalog_match'] is None,'source FE/null actor orLil voice3 without catalogue substitution')
            boundary=next(b for b in fresh['boundaries'] if b['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'))
            require(boundary['text_hex']==native['bodies']['revised_English'][d['id']]['expanded_body'].hex(),'final source dispatch macro expansion matches independent native body')
            require((len(fresh['FE_original_null_actor_calls'])==1 and fresh['FE_original_null_actor_calls'][0]['args'][2]==0) if is_FE else not fresh['FE_original_null_actor_calls'],'original FE null-actor call distinction')
        require(not ctx.machines,'all native dispatch andentry machines released')
    for fresh,declared,src in zip(rebuilt['groups'],data['relocation']['groups'],source['groups'],strict=True):
        number=fresh['block'];require(number==declared['block']==src['block'] and not fresh['relative_fixups'] and not declared['relocated_skip_cases'],'complete two groups without invented relative sites')
        packet=next(g for g in data['current']['groups'] if g['block']==number);sourcecommands=packet['all_source_commands']
        require(src['all_original_source_commands']==sourcecommands,'all original source command extents/bytes')
        require(src['complete_terminal']==sourcecommands[-1],'complete original source terminal identity')
        require(src['complete_source_preambles']==[dict(id=r['id'],source_reference=r['source_reference'],preamble_hex=r['source_complete_preamble_hex']) for r in packet['records']],'all exact source-qualified six-byte preamble references')
        for a,b,c in zip(sourcecommands,fresh['all_current_commands'],fresh['all_target_commands'],strict=True):
            require(a['word']==b['word']==c['word'],'all source/current/final command categories')
            if c['word']==0x4000:
                require(a['whole_command_hex'][:12]==b['whole_command_hex'][:12]==c['whole_command_hex'][:12],'complete six-byte source speech preambles');continue
            require(a['whole_command_hex']==b['whole_command_hex']==c['whole_command_hex'],'opaque source/current/final command andend bytes')
            expected_controls.append(dict(block=number,source_offset=a['offset'],current_offset=b['offset'],target_offset=c['offset'],word=c['word'],complete_source_current_target_hex=c['whole_command_hex'],target_native_extent=c['native_extent']))
        for proof,commands,block in [(src['normal_seeded_ends'],sourcecommands,bytes.fromhex(packet['clean_block_hex'])),(declared['target_seeded_normal_ends'],fresh['all_target_commands'],fresh['target_block'])]:
            terminal=commands[-1];require(terminal['word']==0 and terminal['native_extent']==4 and block[terminal['offset']:terminal['offset']+4]==bytes(4),'full four-byte terminal before independent end evaluation')
            cases=[ends['end_case'](arm,block,terminal['offset'],p,v) for p in [0,1,2,3,0xFFFFFFFF] for v in [0,1,2,3,0xFFFFFFFF]]
            require(cases==proof,'all independently executed complete end/ABI/value-carry fields');endcount+=len(cases)
        structural=src['isolated_original_structural_pairs']
        for command,proof in zip([c for c in sourcecommands if c['word'] not in [0x4000,0]],structural,strict=True):
            raw=bytes.fromhex(command['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw
            require((proof['source_offset'],proof['source_command_hex'],proof['word'])==(command['offset'],raw.hex(),command['word']),'source-qualified isolated opaque command')
            require([v['version'] for v in proof['versions']]==['clean-decoder','current-decoder'],'both original opaque decoder versions')
            for v in proof['versions']:
                code=arm if v['version']=='current-decoder' else cleanarm
                require(v==dict(version=v['version'],**walk(code,isolated)),'independent opaque structural decoder/bridge scope');opaque+=1
    require(expected_controls==controls['nontext_commands'] and len(expected_controls)==9 and endcount==100 and opaque==14,'all nine nontext commands/100 source-target ends/seven paired opaque structural decodes')
    for key in ['all15_commands_six_preambles_source_FE_one_FI_nine_nonspeech_commands_full_ends_andtails_preserved','source_61FF_6302_6000_633D_623D_two_A000_bodies_exact','native_dispatch_UI_bodies_unexecuted_not_actual_geometry_orfull_effect_semantics','fifty_target_seeded_end_cases_bound_to_relocation']:
        require(controls[key] is True,'native control scope:'+key)
    require(source['B47_excludes48_B48_no_exclusion_not_mutual_exclusion_orfull_chronology'] and source['seven_effect_bodies_structurally_decoded_with_disclosed_bridges_not_gameplay_semantics'] and source['native_entry_not_outer_eligibility_oractual_event_activation'],'source entry/effect scope preserved')
    return dict(independent_final_dispatches=6,independent_EV1_entries=2,source_target_seeded_end_cases=100,paired_opaque_structural_decodes=14,nontext_commands=9,relative_andquery_sites=0,native_UI_boundaries_not_new_actual_scene_orouter_eligibility=True)

def check_loaders_and_census(data,parent,reference,rebuilt,load,require):
    loader,caller=data['loaders'],data['callers']
    for key in ['all_original_EV1_actions_select_block_indices_not_interior_offsets','both_original_parent_modes_begin_payload_plus8','all_payload_cache_metadata_neighbor_guards_SP_PC_andABI_exact','original_executed_instructions_exact_only_SDK_IO_bridges','controlled_native_route_global_inputs_not_ordinary_event_activation']:
        require(loader[key] is True,'original loader scope:'+key)
    for key in ['all_shipped_decoded_units_andwhole_ARM9_components_byte_exact_to_registered_parent','only_original24070_interpreter_call_no_literal_alias','all_original_EV1_block_indices325_loads650_parent_modes_verified','all15_source_current_target_commands_zero_relative_sites6_complete_preambles_bound','no_interior_entries_unmapped_nested_targets_orunowned_component_changes','exact_code_census_reuse_not_a_second_fresh_census','source_reference_scope_not_arbitrary_dynamic_pointer_orall_attainable_paths_proof']:
        require(caller[key] is True,'original caller scope:'+key)
    loads,modes=load(loader['load_proof']),load(loader['parent_mode_proof'])
    require(loads['ROM_sha256']==modes['ROM_sha256']==loader['research_ROM_sha256']==caller['research_ROM_sha256']==sha(bytes(reference.rom.save())),'all loader/caller proofs exact tested ROM ownership')
    require(loader['parent_sha256']==caller['parent_sha256']==sha(bytes(parent.rom.save())),'loader/caller exact registered parent ownership')
    prior=load(caller['exact_reused_same_complete_code_census'])
    require(sha(Path(caller['exact_reused_same_complete_code_census']).read_bytes())==caller['exact_reused_same_complete_code_census_sha256'] and prior['native_call_census']['research']==caller['native_call_census'] and caller['fresh_caller_censuses']==1,'one fresh census andexact prior complete-code association')
    return original_loaders(data,parent,reference,rebuilt,load,require)
