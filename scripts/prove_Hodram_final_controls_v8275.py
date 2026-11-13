"""Bind28 final dispatches/24nonrelative controls, six raw query evaluations andoriginal4800/4700 boundaries."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.gerhard_surname_profile_v1 import validate_name_transition
from scripts.Hodram_target_route_context_v8270 import RouteCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_final_controls_v8275')
CURRENT=Path('work/analysis/Hodram_current_review_binding_v8272/28_exact_current_refs_registered_name_dependency_andnative_reuse.json')
MAP=Path('work/analysis/Hodram_three_block_relocation_v8273/three_blocks28_speeches8_relative_sites40_native_cases_full_inverses.json')
STORED=Path('work/analysis/Hodram_three_block_stored_v8274/28_stored_bodies44_fresh68_reused_alignments28_exact_native_pages.json')
EFFECTIVE=Path('work/analysis/Hodram_B137_B45_B46_effective_v8240/all28_effective_English_templates56_original_dispatches_no_FE.json')
NAMES=Path('work/analysis/Hodram_target_names_v8271/six_current_identities12_getters6_native_nameplanes_own_captain1_context.json')
SOURCE=Path('work/analysis/Hodram_B137_B45_B46_source_controls_v8188/three_EV1_entries60_commands28_speeches_native_relative_predicate_and75_seeded_ends.json')
PICTURE=Path('work/analysis/Hodram_B46_pigment_v8190b/original4800_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json')
INPUT=Path('work/analysis/current_V8259_Hodram_native_v8270/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();current,mapping,stored,effective,names,source,picsource=map(read,[CURRENT,MAP,STORED,EFFECTIVE,NAMES,SOURCE,PICTURE])
    assert stored['relocation_sha256']==sha(MAP.read_bytes()) and names['candidate_sha256']==mapping['candidate_sha256']==current['current_ROM_sha256']
    image=NdsImage.open(current['current_ROM']);arm=image.read_file('/__arm9__.bin');inverse=validate_name_transition(NdsImage.open('out/all_routes_combined_v8172_candidate.nds').read_file('/__arm9__.bin'),arm)
    bank=IlnkContainer.parse(Path(mapping['target_archive']).read_bytes()).blocks
    voices={r['source_selector']:r['original_voice_class'] for r in names['native_six_source_voices']['rows']}
    ns={**inherited.__dict__,'SOURCE':CURRENT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    adapters=dict(effective['source_owned_dispatch_adapters'])
    adapters['bind_current_catalog']=checked_text(adapters['bind_current_catalog'],{"sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'":"sha(arm)=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'"})
    for name,text in adapters.items():exec(compile(text,__file__+'::unchanged-original-'+name,'exec'),ns)
    exec(compile(effective['source_owned_measured_macro_body_adapter'],__file__+'::unchanged-measured-Hodram-defaults','exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    pe=dict(picture.__globals__);exec(compile(picsource['source_owned_picture_adapter'],__file__+'::unchanged-source4800','exec'),pe)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    dispatches=[];controls=[];queries=[];ends=[];piccases=[]
    for group in mapping['groups']:
        number=group['block'];spec=next(g for g in current['groups'] if g['block']==number);block=bank[number]
        clean,previous=bytes.fromhex(spec['clean_block_hex']),bytes.fromhex(spec['current_block_hex']);assert sha(block)==group['target_block_sha256']
        for ref in group['text_records']:
            at=ref['new_offset'];raw=bytes.fromhex(ref['target_hex']);assert block[at:at+len(raw)+1]==raw+b'\0'
            result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
            boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body')
            expected=next(r for r in stored['records'] if r['id']==ref['id'])['expanded_stored_hex']
            assert boundary['text_hex']==expected and result['resolved_actor_ID']==raw[0] and result['source_voice_class']==voices[raw[0]] and not result['FE_original_null_actor_calls']
            assert result['registered_catalog_match'] is None
            dispatches.append(dict(id=ref['id'],block=number,final_offset=at,final_stored_hex=raw.hex(),**result))
        for a,b,c,m in zip(spec['all_source_commands'],spec['all_current_commands'],group['all_target_commands'],group['command_map'],strict=True):
            assert a['word']==b['word']==c['word']==m['word'];word=c['word']
            if word in [0x4000,0x100,0x200,0x300,0x400]:continue
            assert a['whole_command_hex']==b['whole_command_hex']==c['whole_command_hex']
            controls.append(dict(block=number,source_offset=a['offset'],previous_offset=b['offset'],target_offset=c['offset'],word=word,source_current_target_command_hex=c['whole_command_hex']))
            if word in [0x8000,0x8100]:
                values=[]
                for version,payload,command in [('clean',clean,a),('current',previous,b),('target',block,c)]:
                    value=ctx.execute(probe,payload,command);ctx.machines.pop();values.append(dict(version=version,**value))
                assert values[0]['native_result']==values[1]['native_result']==values[2]['native_result']
                queries.append(dict(block=number,source_offset=a['offset'],current_offset=b['offset'],target_offset=c['offset'],cases=values,raw_results_not_boolean_menu_orpath_attainability=True))
            if word in [0x4800,0x4700]:
                value=ctx.execute(pe['picture'] if word==0x4800 else picture,block,c);ctx.machines.pop()
                if word==0x4800:
                    assert value['original_picture_boundary_calls']==picsource['native_picture_case']['original_picture_boundary_calls']
                    assert value['original_picture_boundary_calls'][0]['descriptor']==[0,181,1,5] and value['original_picture_boundary_calls'][0]['layout']==[0,0,0]
                piccases.append(dict(block=number,**value))
        prior=next(g for g in source['groups'] if g['block']==number)
        assert spec['all_source_commands'][-1]==prior['source_terminal'] and spec['all_current_commands'][-1]['offset']==prior['source_terminal']['offset']
        assert clean[prior['source_terminal']['offset']:prior['source_terminal']['offset']+4]==previous[prior['source_terminal']['offset']:prior['source_terminal']['offset']+4]==bytes(4)
        ends.append(dict(block=number,source_andcurrent_same_four_byte_end_exact_reuse=prior['normal_seeded_ends'],target_cases_exact_reuse=group['target_seeded_normal_ends'],
            target_terminal=group['all_target_commands'][-1],source_proof=str(SOURCE),relocation_proof=str(MAP),no_repeated_seeded_end_calls=True))
    assert len(dispatches)==28 and len(controls)==24 and len(queries)==2 and len(piccases)==2 and not ctx.machines
    assert sorted(p['source_command_hex'] for p in piccases)==['0047','0048b5a8']
    save(ROOT/'28_final_dispatches24_controls6_raw_evaluations_original4800_4700_requests.json',dict(candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],
        relocation=str(MAP),relocation_sha256=sha(MAP.read_bytes()),stored=str(STORED),stored_sha256=sha(STORED.read_bytes()),complete_ARM9_name_inverse=inverse,
        final_dispatches=dispatches,original_nonrelative_nontext_control_maps=controls,raw_predicates_andqueries=queries,fresh_raw_native_evaluations=6,
        picture_andhide_boundary_cases=piccases,fresh_picture_andhide_native_boundary_cases=2,
        original4800_descriptor181_layout0_0_0_not_Rafael4821_layout2=True,original4700_hide_request_not4720=True,
        normal_end_cases_exact_reused=ends,source_seeded_ends_reused=75,target_seeded_ends_reused=75,no_fresh_seeded_end_calls=True,
        target_relative_native_cases_exact_reused=40,all60_commands28_preambles8_relative_sites2_rawqueries_andwhole_terminals_preserved=True,
        registered_current_catalogue_binding=catalogue,source_owned_dispatch_adapters=adapters,
        no_global_guard_profile_code_font_orcatalogue_change=True,
        all28_original_static_actors_voices_andcomplete_final_body_dispatches_match=True,all_final_target_bodies_no_old_catalogue_matches=True,
        source_zero_FI_FA_FO_no_macros_added=True,ordinary_opening_raw_queries_not_natural_scene_activation_orforced_state=True,
        full_opaque_A000_picture_resource_hide_UI_bodies_not_executed_bythis_native_boundary_probe=True,
        actual_B137_B45_B46_silences_nameheaders_4800_layout0_4700_bounds_andtransitions_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,MAP,STORED,EFFECTIVE,NAMES,SOURCE,PICTURE,INPUT,Path(__file__)]}))
    print('Hodram28 final dispatches/24originalcontrols/sixrawqueryevaluations/4800layout0+4700hide native requests pass;40skipcases/150seededends exactreuse;actualUI pending.')
