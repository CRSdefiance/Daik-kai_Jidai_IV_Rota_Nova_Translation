"""Bind the source EV entry,all relative sites,predicate andcontrol boundaries in own captain0."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B141_controls_v3538b import control630A
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_source_controls_v7870')
SOURCE=Path('work/analysis/Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Rafael_B45_clean_gloss_v7864b/twelve_fresh_clean_exchange_glosses_before_current_English.json')
INPUT=Path('work/analysis/current_V7857_Rafael_native_v7868/current_native_input.json')
NAMES=Path('work/analysis/Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();source,gloss,inp,names=map(read,[SOURCE,GLOSS,INPUT,NAMES])
    assert names['source_gloss_sha256']==sha(GLOSS.read_bytes()) and names['current_English_B45_bodies_still_unread']
    current,clean=[NdsImage.open(p) for p in [inp['current_ROM'],source['source_ROM']]]
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']==names['candidate_sha256']
    arm=current.read_file('/__arm9__.bin');ja_arm=clean.read_file('/__arm9__.bin')
    spans=[(0x23840,0x23A28),(0x293B8,0x2976C),(0x29874,0x29A9C),(0x2A414,0x2A600),(0x24048,0x24118)]
    assert all(arm[a:b]==ja_arm[a:b] for a,b in spans)
    ev=current.read_file('/data/EV0.DK4');assert ev==clean.read_file('/data/EV0.DK4') and sha(ev)==source['EV0_sha256']
    group=source['groups'][0];block=bytes.fromhex(group['clean_block_hex']);commands=group['commands']
    assert len(block)==764 and group['clean_logical_end']==762 and block[762:]==bytes(2)
    selected=group['source_event_records'];assert len(selected)==1
    assert [(r['event_ID'],r['action_index'],r['script_block'],r['must_be_completed'],r['must_not_be_completed']) for r in selected]==[(45,46,45,[],[])]
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    entry_adapter=checked_text(inspect.getsource(native_entry),{
        'assert get(0x7F244)==2':'assert get(0x7F244)==0',
        'not_current_eligibility_or_selected_B234_activation':'not_current_eligibility_or_selected_B45_activation'})
    env=dict(native_entry.__globals__);exec(compile(entry_adapter,__file__+'::source-EV0-own-captain0','exec'),env)
    entry=ctx.execute(env['native_entry'],ev,selected);ctx.machines.pop()
    boundaries={c['offset'] for c in commands}|{group['clean_logical_end']};branches=[]
    for c in commands:
        if c['word'] not in [0x100,0x200,0x300,0x400]:continue
        result=ctx.execute(native_skip,block,c);ctx.machines.pop()
        assert all(r['next_offset'] in boundaries for r in result['cases'])
        branches.append(dict(block=45,**result))
    assert len(branches)==5 and sum(len(c['cases']) for c in branches)==25
    condition=next(c for c in commands if c['word']==0x8000)
    assert condition['offset']==568 and condition['whole_command_hex']=='0080ffff14000cb0'
    predicate=ctx.execute(probe,block,condition);ctx.machines.pop()
    words=[0x6300,0x6328,0x632B]
    resource_adapter=checked_text(inspect.getsource(control630A),{
        'previous,boundary_return):':'previous,boundary_return,word):',
        "value=bytes.fromhex('0a63')":"assert word in SOURCE_RESOURCE_WORDS;value=struct.pack('<H',word)",
        '[0x02386EFC,10,2,1]':'[0x02386EFC,word&255,2,1]'})
    env={**control630A.__globals__,'SOURCE_RESOURCE_WORDS':words};exec(compile(resource_adapter,__file__+'::three-original-resource-words','exec'),env)
    resources=[]
    for word in words:
        assert any(c['word']==word for c in commands)
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for incidental in [0,0xFFFFFFFF]:
                resources.append(ctx.execute(env['control630A'],previous,incidental,word));ctx.machines.pop()
    structural=[]
    for c in commands:
        if c['word'] not in [0x61FF,0xC281]:continue
        raw=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw
        versions=[]
        for label,a in [('clean-decoder',ja_arm),('current-decoder',arm)]:
            result=walk(a,isolated);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
            assert len(result['rows'])==1 and result['rows'][0]['native_extent']==2
            versions.append(dict(version=label,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
        structural.append(dict(word=c['word'],original_offset=c['offset'],source_command_hex=c['whole_command_hex'],versions=versions))
    end=commands[-1];assert end['word']==0 and end['offset']==758 and end['native_extent']==4 and block[758:762]==bytes(4)
    ends=[end_case(arm,block,758,previous,seed) for previous in [0,1,2,3,0xFFFFFFFF] for seed in [0,1,2,3,0xFFFFFFFF]]
    assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
    assert len(resources)==30 and len(structural)==2 and not ctx.machines
    save(ROOT/'source_EV0_five_relative_sites_predicate_resources_structural_andnormal_end.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        source_EV0_sha256=sha(ev),selected_source_event_records=selected,native_source_event_getters=entry,
        source_owned_event_adapter=entry_adapter,source_relative_sites=branches,source_relative_cases=25,
        source_predicate=predicate,source_predicate_exact_operand_hex=condition['whole_command_hex'],
        original_predicate_evaluated_in_current_opening_not_natural_Ceuta_eligibility=True,
        resource_words=words,original_resource_boundary_cases=resources,source_owned_resource_adapter=resource_adapter,
        isolated_source_61FF_C281_structural_cases=structural,normal_seeded_end_cases=ends,
        original_complete_four_byte_end_andseparate_two_zero_tail_bytes=True,
        all24_commands_twelve_speeches_andFE_branch_retained=True,
        FE_R52_only_entered_when_previous_predicate_result_is1_at0300=True,
        unconditional0100_wrapper_skips_FE_body_for_other_structural_results=True,
        source_control_boundary_tests_do_not_prove_resource_callee_effects_C281_display_orfull_trade_mechanics=True,
        no_ROMS_RAM_savestate_controller_event_flag_roster_role_funds_orRNG_gameplay_forcing=True,
        synthetic_previous_results_andseeded_end_cases_are_isolated_decoder_inputs_only=True,
        actual_B45_selection_FE_pagination_percent_andtransition_capture_pending=True,
        current_B45_English_bodies_still_unread=True,
        source_current_handler_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        source_owned_skip_probe=inspect.getsource(native_skip),source_owned_predicate_probe=inspect.getsource(probe),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,INPUT,NAMES,Path(__file__)]},full_goal_complete=False))
    print('Source EV0event45/action46;5relative sites/25guarded cases,one original8000 predicate,30resource boundaries,two isolated61FF/C281 pairs,25normal carry ends pass.')
    print('Predicate in opening',predicate['native_result'],'FE condition result1;not natural eligibility orfull effect/display proof.Current English unread.')
