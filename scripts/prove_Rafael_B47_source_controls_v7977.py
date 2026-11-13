"""Bind source entry,24 relative sites,six raw predicates andcomplete normal-end carry."""
import inspect,struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_source_controls_v7977')
SOURCE=Path('work/analysis/Rafael_next_clean_v7971/complete_clean_SC0_B47_EV0_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Rafael_B47_clean_gloss_v7973/15_fresh_clean_glosses_complete_B37_context_before_current_English.json')
INPUT=Path('work/analysis/current_V7964_Rafael_native_v7967/current_native_input.json')
NAMES=Path('work/analysis/Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();source,gloss,inp,names=map(read,[SOURCE,GLOSS,INPUT,NAMES])
    assert names['source_gloss_sha256']==sha(GLOSS.read_bytes()) and names['current_English_B47_bodies_still_unread']
    current,clean=[NdsImage.open(p) for p in [inp['current_ROM'],source['source_ROM']]]
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']==names['candidate_sha256']
    assert sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    arm,ja_arm=[im.read_file('/__arm9__.bin') for im in [current,clean]]
    spans=[(0x23840,0x23A28),(0x293B8,0x2976C),(0x29874,0x29A9C),(0x2A414,0x2A600),(0x24048,0x24118)]
    assert all(arm[a:b]==ja_arm[a:b] for a,b in spans)
    ev=current.read_file('/data/EV0.DK4');assert ev==clean.read_file('/data/EV0.DK4') and sha(ev)==source['EV0_sha256']
    g=source['groups'][0];block=bytes.fromhex(g['clean_block_hex']);commands=g['commands']
    assert len(block)==g['clean_logical_end']==1284 and g['clean_tail_bytes']==0 and len(commands)==48 and len(g['records'])==15
    assert all(r['current_English_body_unread'] for r in gloss['records'])
    assert all(bytes.fromhex(r['source_hex'])[1:].count(t)==0 for r in g['records'] for t in [b'FI',b'FA',b'FO'])
    selected=g['source_event_records']
    assert [(r['event_ID'],r['action_index'],r['script_block'],r['must_be_completed'],r['must_not_be_completed']) for r in selected]==[(47,48,47,[37],[])]
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    adapter=checked_text(inspect.getsource(native_entry),{
        'assert get(0x7F244)==2':'assert get(0x7F244)==0',
        'not_current_eligibility_or_selected_B234_activation':'not_current_eligibility_or_selected_B47_activation'})
    env=dict(native_entry.__globals__);exec(compile(adapter,__file__+'::original-EV0-entry','exec'),env)
    entry=ctx.execute(env['native_entry'],ev,selected);ctx.machines.pop()
    boundaries={c['offset'] for c in commands}|{1284};branches=[];operands=[];predicates=[]
    for c in commands:
        if c['word'] in [0x100,0x200,0x300,0x400]:
            result=ctx.execute(native_skip,block,c);ctx.machines.pop()
            assert all(r['next_offset'] in boundaries for r in result['cases'])
            branches.append(dict(block=47,**result))
            at=c['offset'];span=struct.unpack_from('<H',block,at+2)[0]
            operands.append(dict(block=47,offset=at,word=c['word'],span_field_offset=at+2,source_span=span,
                unmatched_next_offset=at+4,matched_skip_target=at+4+span,ancestor_0100_offsets=c['ancestor_0100_offsets'],
                source_operand_hex=block[at:at+4].hex()))
        elif c['word']==0x8000:
            result=ctx.execute(probe,block,c);ctx.machines.pop();predicates.append(result)
            print('Predicate',c['offset'],c['whole_command_hex'],result['native_result'],flush=True)
    assert len(branches)==24 and sum(len(r['cases']) for r in branches)==120 and len(predicates)==6
    same={}
    for p in predicates:
        same.setdefault(p['source_command_hex'],p['native_result'])
        assert same[p['source_command_hex']]==p['native_result']
    assert len(same)==4
    structural=[]
    for c in commands:
        if c['word'] not in [0x61FF,0xA000]:continue
        raw=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw
        versions=[]
        for label,a in [('clean-decoder',ja_arm),('current-decoder',arm)]:
            result=walk(a,isolated)
            assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1
            assert result['rows'][0]['native_extent']==c['native_extent']
            versions.append(dict(version=label,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
        structural.append(dict(word=c['word'],source_offset=c['offset'],source_command_hex=c['whole_command_hex'],versions=versions))
    assert len(structural)==2 and [c['source_command_hex'] for c in structural]==['ff61','00a0ffff010c2160']
    end=commands[-1];assert end['word']==0 and end['offset']==1280 and end['native_extent']==4 and block[1280:]==bytes(4)
    ep=Path('work/analysis/lil_B218_controls_v6878/two_A000_structural_cases50_normal_seeded_ends_no_relative_or_predicate.json')
    end_adapter=read(ep)['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__)
    exec(compile(end_adapter,__file__+'::source-normal-end-value-carry','exec'),env)
    ends=[env['end_case'](arm,block,1280,p,s) for p in [0,1,2,3,0xFFFFFFFF] for s in [0,1,2,3,0xFFFFFFFF]]
    assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends) and not ctx.machines
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);dis=ROOT/'exact_original_expression_andcommand_handlers.txt'
    dis.write_text('\n'.join(f'{i.address:08X} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for a,b in spans for i in decoder.disasm(arm[a:b],0x02000000+a))+'\n',encoding='utf8')
    save(ROOT/'source_EV0_24_relative_sites120_cases6_raw_predicates25_seeded_ends.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        source_event_records=selected,current_native_EV_entry=entry,source_relative_cases=branches,
        operands_requiring_adjustment_when_resizing=operands,source_raw_predicates=predicates,unique_raw_predicate_results=same,
        source_terminal=end,normal_seeded_ends=ends,isolated_original_structural_pairs=structural,
        source_8000_returns_raw_evaluator_value_not_assumed_boolean=True,
        actual_opening_predicate_values_not_natural_B47_activation_orall_possible_values=True,
        native_entry_is_not_prerequisite_satisfaction_orcurrent_eligibility_oractual_activation=True,
        isolated_source_A000_effect_body_bridged_not_gameplay_orcomplete_semantics=True,
        all48_commands15_complete_preambles_andcomplete_normal_end_preserved=True,
        current_B47_English_bodies_still_unread=True,branch_composition_andpredicate_semantics_pending=True,
        no_gameplay_state_condition_roster_role_funds_seed_orresult_forced=True,
        disassembly=str(dis),disassembly_sha256=sha(dis.read_bytes()),
        unchanged_source_runtime_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        source_owned_entry_adapter=adapter,source_owned_skip_probe=inspect.getsource(native_skip),
        source_owned_predicate_probe=inspect.getsource(probe),source_owned_seeded_end_adapter=end_adapter,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,INPUT,NAMES,ep,Path(__file__)]},
        new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('B47 source:24 relative sites/120 cases,6 raw predicates,25 seeded ends,2 original structural pairs;current English unread.')
