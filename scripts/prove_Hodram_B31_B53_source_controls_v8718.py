"""Map complete clean B31/B53 controls in the own verified V8704 captain1 context.

Original raw query results and event getters are unforced. Five branch arguments
and seeded end values are separate disposable structural cases, not gameplay.
Opaque action bridges are recorded as structure, not invented effect semantics.
"""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B52_registered_route_context_v8707 import RouteCurrentContext
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.research_wedding_command_v676 import walk
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B31_B53_source_controls_v8718')
GLOSS=Path('work/analysis/Hodram_B31_B53_clean_context_v8714/three_clean_glosses_explicit52_31_53_dependency_andunnamed_man_before_current_English.json')
BASE_SOURCE=Path('work/analysis/Hodram_B53_clean_v8711/complete_clean_SC1_B53_EV1_andcoverage_before_current_English.json')
INPUT=Path('work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json')
PREVIOUS=Path('work/analysis/Hodram_B52_source_controls_v8620/source_controls.json')

if __name__=='__main__':
    assert not ROOT.exists();gloss,base,inp,prior=map(read,[GLOSS,BASE_SOURCE,INPUT,PREVIOUS])
    assert gloss['all_three_complete_clean_utterances_glossed_before_earlier_English'] and gloss['current_English_for_B31_andB53_still_unconsulted']
    image=NdsImage.open(inp['current_ROM']);clean=NdsImage.open('work/clean.nds')
    arm,ja=image.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    assert inp['registered_profile']=='all-routes-unified-v8704' and sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256'] and sha(Path('work/clean.nds').read_bytes())==base['source_ROM_sha256']
    spans=prior['unchanged_source_runtime_spans']
    assert all(arm[s['start']:s['end']]==ja[s['start']:s['end']] and sha(arm[s['start']:s['end']])==s['sha256'] for s in spans)
    ev=image.read_file('/data/EV1.DK4');assert ev==clean.read_file('/data/EV1.DK4') and sha(ev)==base['EV1_sha256']
    events={}
    for group in gloss['groups']:
        for e in group['source_event_anddependencies']:
            assert e['event_ID'] not in events or events[e['event_ID']]==e;events[e['event_ID']]=e
    events=[events[key] for key in sorted(events)]
    assert [e['event_ID'] for e in events]==[31,52,53,74]
    inventory,walker,inventory_source=scoped_inventory()
    entry_adapter=checked_text(prior['source_owned_entry_adapter'],{
        'not_current_eligibility_or_selected_Hodram_B52_activation':'not_current_eligibility_or_selected_Hodram_B31_B53_activation'})
    entry_env=dict(native_entry.__globals__);exec(compile(entry_adapter,__file__+'::entry-ownV8704','exec'),entry_env)
    end_adapter=prior['source_owned_seeded_end_adapter'];end_env=dict(end_case.__globals__)
    exec(compile(end_adapter,__file__+'::complete-original-normal-end','exec'),end_env)
    seeds=[e for e in prior['distinct_seeded_ends'] if not e['flagged_terminal']]
    assert len(seeds)==25 and len({(e['previous_result'],e['initial_value_word']) for e in seeds})==25
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    entry=ctx.execute(entry_env['native_entry'],ev,events);ctx.machines.pop()
    groups=[]
    for source in gloss['groups']:
        number=source['block'];block=bytes.fromhex(source['clean_block_hex']);commands=source['commands'];logical=source['clean_logical_end']
        assert number in [31,53] and len(block)==logical==source['clean_stored_bytes'] and source['clean_tail_bytes']==0
        decoded,speeches=inventory(arm,block);assert decoded==commands and len(speeches)==len(source['records'])
        boundaries={c['offset'] for c in commands}|{logical};branches=[];operands=[];queries=[];opaque=[]
        for command in commands:
            word,at=command['word'],command['offset']
            if word in [0x100,0x200,0x300,0x400]:
                span=struct.unpack_from('<H',block,at+2)[0];assert at+4 in boundaries and at+4+span in boundaries
                result=ctx.execute(native_skip,block,command);ctx.machines.pop()
                assert all(c['next_offset'] in boundaries and c['next_offset']==(at+4+span if c['taken'] else at+4) for c in result['cases'])
                branches.append(result)
                operands.append(dict(block=number,offset=at,word=word,span_field_offset=at+2,source_span=span,
                    unmatched_next_offset=at+4,matched_skip_target=at+4+span,ancestor_0100_offsets=command['ancestor_0100_offsets'],source_operand_hex=block[at:at+4].hex()))
            elif word in [0x8000,0x8100]:
                result=ctx.execute(probe,block,command);ctx.machines.pop();assert result['native_result'][0]==2 and result['no_predicate_or_event_flag_forced'];queries.append(result)
            elif word not in [0,0x4000]:
                assert word!=0x2100 and word not in [0x4820,0x4800,0x4700]
                raw=bytes.fromhex(command['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw
                versions=[]
                for label,code in [('clean-decoder',ja),('current-decoder',arm)]:
                    result=walk(code,isolated)
                    assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['native_extent']==command['native_extent']
                    versions.append(dict(version=label,**result))
                assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
                opaque.append(dict(source_offset=at,word=word,source_command_hex=raw.hex(),versions=versions))
        terminal=commands[-1];assert terminal['word']==0 and terminal['native_extent']==4 and terminal['whole_command_hex']=='00000000' and terminal['offset']+4==logical
        ends=[end_env['end_case'](arm,block,terminal['offset'],c['previous_result'],c['initial_value_word']) for c in seeds]
        assert len(ends)==25 and all(e['native_result']==[0,e['initial_value_word'],0,0,0,0] and e['all4MiB_owner_input_ABI_output_and_length_guards_exact'] for e in ends)
        if number==31:
            assert (len(commands),len(speeches),len(branches),sum(len(r['cases']) for r in branches),len(queries),len(opaque))==(9,2,4,20,1,1)
            assert [(r['source_offset'],r['word']) for r in opaque]==[(8,0x6311)]
        else:
            assert (len(commands),len(speeches),len(branches),len(queries),len(opaque))==(9,1,0,0,7)
            assert [(r['source_offset'],r['word']) for r in opaque]==[(8,0x6000),(10,0x633F),(98,0xA000),(106,0xA000),(114,0xA000),(122,0xA000),(130,0x623F)]
        groups.append(dict(block=number,file_path='/data/SC1.DK4',clean_block_sha256=sha(block),clean_block_hex=block.hex(),
            all_original_source_commands=commands,complete_source_preambles=[dict(id=r['id'],source_reference=r['source_reference'],preamble_hex=r['source_complete_preamble_hex']) for r in source['records']],
            source_event_records=source['source_event_records'],source_relative_cases=branches,operands_requiring_adjustment_when_resizing=operands,
            source_raw_query_cases=queries,paired_opaque_structural_decodes=opaque,normal_seeded_ends=ends,source_terminal=terminal,
            separate_tail_bytes=0,source_macro_counts={m:sum(r['source_Japanese'].count(m) for r in source['records']) for m in ['FI','FA','FO']}))
        print('SOURCE_CONTROL',number,'branches',len(branches),'queries',[q['native_result'] for q in queries],'normal-ends',len(ends),'opaque-pairs',len(opaque),flush=True)
    assert len(groups)==2 and sum(len(g['complete_source_preambles']) for g in groups)==3 and not ctx.machines
    save(ROOT/'source_controls.json',dict(candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),base_source=str(BASE_SOURCE),base_source_sha256=sha(BASE_SOURCE.read_bytes()),
        groups=groups,source_event_anddependency_records=events,original_EV1_entry=entry,
        complete_source_commands=18,complete_speech_preambles=3,relative_sites=4,native_relative_cases=20,raw_unforced_query_cases=1,opaque_structural_decode_pairs=8,normal_seeded_end_cases=50,
        explicit_event_chain=[52,31,53],event53_excludes74=True,
        raw8000_result_not_assumed_boolean_orinvented_plot_predicate=True,
        normal_ends192_and132_preserve_carried_values_all6words_andguards=True,
        opaque6000_6311_633F_623F_A000_effect_semantics_not_invented=True,
        current_B31_B53_English_dialogue_bodies_still_unconsulted=True,
        source_speakers_name_getters_glyphs_fullheaders_branch_context_current_prose_actual_andrelease_pending=True,
        source_owned_entry_adapter=entry_adapter,source_owned_seeded_end_adapter=end_adapter,source_owned_skip_probe=inspect.getsource(native_skip),source_owned_query_probe=inspect.getsource(probe),
        inventory_walker=walker,inventory_function=inventory_source,unchanged_source_runtime_spans=spans,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        offline_native_calls_andstructural_arguments_not_actual_gameplay_orouter_activation=True,
        no_historical_RAM_overlay_source_ROM_edit_new_emulator_run_orcredit=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [GLOSS,BASE_SOURCE,INPUT,PREVIOUS,__file__]}))
    print('B31/B53 source:18commands/3preambles/20branchcases/1unforcedquery/8opaque pairs/50whole normalends inownV8704. EarlierEnglish unread;source display/name/context/actual review pending;zero credit.')
