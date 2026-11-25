"""Bind both whole clean race outcomes to current Hodram EV1/native extents and end carry.

Opaque effects are decoded with disclosed bridges; this does not execute their
gameplay semantics or prove natural event eligibility. No current dialogue read.
"""
import inspect,struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B49_registered_route_context_v8478 import RouteCurrentContext
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from dk4tool.patch.hodram_B49_native_guards_v1 import trusted_adapter
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.research_wedding_command_v676 import walk
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_source_controls_v8486')
GLOSS=Path('work/analysis/Hodram_B50_clean_gloss_v8483/three_first_clean_glosses_gift_andoutgoing_wristband.json')
INPUT=Path('work/analysis/current_V8475_Hodram_native_v8478/current_native_input.json')
END=Path('work/analysis/lil_B218_controls_v6878/two_A000_structural_cases50_normal_seeded_ends_no_relative_or_predicate.json')
PACKETS=[Path('work/analysis/Hodram_B50_clean_v8482/complete_clean_SC1_B50_EV1_andcoverage_before_current_English.json')]
PICTURE=Path('work/analysis/Hodram_B49_source_controls_v8384/source_controls.json')

if __name__=='__main__':
    assert not ROOT.exists();gloss,inp=map(read,[GLOSS,INPUT]);packets=list(map(read,PACKETS))
    assert gloss['all3_clean_utterances_glossed_before_current_English'] and gloss['current_English_dialogue_bodies_still_unconsulted']
    current,clean=[NdsImage.open(p) for p in [inp['current_ROM'],'work/clean.nds']]
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256'] and sha(Path('work/clean.nds').read_bytes())==packets[0]['source_ROM_sha256']
    arm,ja=[i.read_file('/__arm9__.bin') for i in [current,clean]]
    spans=[(0x23840,0x23A28),(0x293B8,0x2976C),(0x29874,0x29A9C),(0x2A414,0x2A600),(0x24048,0x24118)]
    assert all(arm[a:b]==ja[a:b] for a,b in spans)
    ev=current.read_file('/data/EV1.DK4');assert ev==clean.read_file('/data/EV1.DK4') and all(sha(ev)==p['EV1_sha256'] for p in packets)
    events=[g['source_event_records'][0] for g in gloss['groups']]
    assert [(r['event_ID'],r['action_index'],r['script_block'],r['must_be_completed'],r['must_not_be_completed']) for r in events]==[(50,51,50,[49],[])]
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    adapter=checked_text(inspect.getsource(native_entry),{'assert get(0x7F244)==2':'assert get(0x7F244)==1','not_current_eligibility_or_selected_B234_activation':'not_current_eligibility_or_selected_Hodram_B50_activation'})
    env=dict(native_entry.__globals__);exec(compile(adapter,__file__+'::original-EV1-two-outcomes','exec'),env)
    entry=ctx.execute(env['native_entry'],ev,events);ctx.machines.pop()
    end_adapter=read(END)['source_owned_seeded_end_adapter'];en=dict(end_case.__globals__);exec(compile(end_adapter,__file__+'::complete-normal-end-value-carry','exec'),en)
    picture_adapter=trusted_adapter('picture',read(PICTURE)['source_owned_picture_adapter']);pe=dict(picture.__globals__);exec(compile(picture_adapter,__file__+'::original-item148-andhide','exec'),pe);pictures=[]
    inventory,walker,inventory_source=scoped_inventory();bank=IlnkContainer.parse(clean.read_file('/data/SC1.DK4')).blocks;groups=[]
    for packet,g in zip(packets,gloss['groups'],strict=True):
        number=g['block'];block=bank[number];assert block==bytes.fromhex(g['clean_block_hex']) and packet['groups'][0]['commands']==g['commands']
        commands,speeches=inventory(arm,block);assert commands==g['commands'] and len(speeches)==3
        assert len(commands)==12 and not any(c['word'] in [0x100,0x200,0x300,0x400,0x2100,0x4100,0x8000,0x8100] for c in commands)
        structural=[]
        for command in commands:
            if command['word'] in [0x4000,0]:continue
            if command['word'] in [0x4800,0x4700]:
                result=ctx.execute(pe['picture'],block,command);ctx.machines.pop();pictures.append(dict(word=command['word'],**result));continue
            raw=bytes.fromhex(command['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
            for label,code in [('clean-decoder',ja),('current-decoder',arm)]:
                result=walk(code,isolated)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['native_extent']==command['native_extent']
                versions.append(dict(version=label,**result))
            assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
            structural.append(dict(source_offset=command['offset'],source_command_hex=raw.hex(),word=command['word'],versions=versions))
        end=commands[-1];assert end['word']==0 and end['native_extent']==4 and end['offset']+4==g['clean_logical_end'] and block[end['offset']:end['offset']+4]==bytes(4)
        ends=[en['end_case'](arm,block,end['offset'],p,v) for p in [0,1,2,3,0xFFFFFFFF] for v in [0,1,2,3,0xFFFFFFFF]]
        assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
        assert block[g['clean_logical_end']:]==bytes(g['clean_tail_bytes'])
        groups.append(dict(block=number,clean_block_sha256=sha(block),all_original_source_commands=commands,complete_source_preambles=[dict(id=r['id'],source_reference=r['source_reference'],preamble_hex=r['source_complete_preamble_hex']) for r in g['records']],
            source_macro_counts={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in g['records']) for m in ['FI','FA','FO']},source_FE_count=sum(r['source_selector']==254 for r in g['records']),
            isolated_original_structural_pairs=structural,normal_seeded_ends=ends,complete_terminal=end,separate_tail_bytes=g['clean_tail_bytes'],source_picture_andhide_cases=pictures))
    assert sum(len(g['isolated_original_structural_pairs']) for g in groups)==6 and len(pictures)==2 and [p['word'] for p in pictures]==[0x4800,0x4700] and not ctx.machines
    assert pictures[0]['original_picture_boundary_calls'][0]['descriptor']==[0,148,1,5] and pictures[0]['original_picture_boundary_calls'][0]['layout']==[0,0,0]
    assert pictures[1]['original_picture_boundary_calls'][0]['descriptor'] is None and pictures[1]['original_picture_boundary_calls'][0]['layout'] is None
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);dis=ROOT/'exact_source_EV_andcommand_handlers.txt'
    dis.write_text('\n'.join(f'{i.address:08X} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for a,b in spans for i in decoder.disasm(arm[a:b],0x02000000+a))+'\n',encoding='utf8')
    save(ROOT/'source_controls.json',dict(candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],current_native_input=str(INPUT),source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),groups=groups,original_EV1_entry=entry,
        source_event_records=events,source_relative_sites=0,source_raw_predicates=0,normal_seeded_end_cases=25,all12_source_commands_three_complete_preambles_one_full_end_andtwozero_tail_bound=True,
        event50_requires49_not_outer_eligibility_orfull_chronology=True,six_opaque_effect_bodies_structurally_decoded_with_disclosed_bridges_not_gameplay_semantics=True,
        source_FE_geometry_names_effect_semantics_current_prose_andactual_tests_pending=True,source_picture_andhide_cases=pictures,source_owned_picture_adapter=picture_adapter,item148_native_layout0_andoriginal_hide_boundary_pass=True,current_English_dialogue_bodies_still_unconsulted=True,
        no_runtime_flags_party_roster_role_funds_RNG_conditions_results_orinputs_forced=True,native_entry_not_outer_eligibility_oractual_event_activation=True,
        source_owned_EV1_entry_adapter=adapter,source_owned_seeded_end_adapter=end_adapter,inventory_walker=walker,inventory_function=inventory_source,
        unchanged_source_runtime_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],disassembly=str(dis),disassembly_sha256=sha(dis.read_bytes()),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,INPUT,END,PICTURE,*PACKETS,Path(native_entry.__code__.co_filename),Path(end_case.__code__.co_filename),Path(walk.__code__.co_filename),Path(__file__)]}))
    print('B50source:12commands/3preambles/1EV1entry/6pairedopaque decodes/25normalends/item148layout0andhide pass;FE/native effects/currentEnglish pending.')
