"""Bind clean B50's native EV0 entry, full source structure and seeded normal value carry before English exposure."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_source_controls_v8132')
SOURCE=Path('work/analysis/Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Rafael_B50_clean_gloss_v8131/28_first_clean_glosses_three_source_identities_before_current_English.json')
INPUT=Path('work/analysis/current_V8066_Rafael_native_v8069/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();source,gloss,inp=map(read,[SOURCE,GLOSS,INPUT])
    assert gloss['source_packet_sha256']==sha(SOURCE.read_bytes()) and gloss['source_only_no_current_B50_English_exposed_no_localized_manuscript']
    current,clean=[NdsImage.open(p) for p in [inp['current_ROM'],source['source_ROM']]]
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']
    assert sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    arm,ja_arm=[im.read_file('/__arm9__.bin') for im in [current,clean]]
    spans=[(0x23840,0x23A28),(0x293B8,0x2976C),(0x29874,0x29A9C),(0x2A414,0x2A600),(0x24048,0x24118)]
    assert all(arm[a:b]==ja_arm[a:b] for a,b in spans)
    ev=current.read_file('/data/EV0.DK4');assert ev==clean.read_file('/data/EV0.DK4') and sha(ev)==source['EV0_sha256']
    g=source['groups'][0];block=bytes.fromhex(g['clean_block_hex']);commands=g['commands']
    assert len(block)==1520 and g['clean_logical_end']==1518 and g['clean_tail_bytes']==2 and block[1518:]==bytes(2)
    assert len(commands)==37 and len(g['records'])==28
    assert all(r['current_B50_English_body_still_unread'] for r in gloss['records'])
    counts={t.decode():sum(bytes.fromhex(r['source_hex'])[1:].count(t) for r in g['records']) for t in [b'FI',b'FA',b'FO']}
    assert counts==dict(FI=1,FA=2,FO=0)
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100] for c in commands)
    selected=g['source_event_records'];assert [(e['event_ID'],e['category'],e['action_index'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in selected]==[(50,5,51,50,[],[])]
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    adapter=checked_text(inspect.getsource(native_entry),{'assert get(0x7F244)==2':'assert get(0x7F244)==0','not_current_eligibility_or_selected_B234_activation':'not_current_eligibility_or_selected_B50_activation'})
    env=dict(native_entry.__globals__);exec(compile(adapter,__file__+'::original-EV0-B50-entry','exec'),env)
    entry=ctx.execute(env['native_entry'],ev,selected);ctx.machines.pop()
    inventory,walker,inventory_source=scoped_inventory();original_current,speeches=inventory(arm,block)
    assert original_current==commands and len(speeches)==28
    end=commands[-1];assert end['word']==0 and end['offset']==1514 and end['native_extent']==4 and block[1514:1518]==bytes(4)
    previous=Path('work/analysis/lil_B218_controls_v6878/two_A000_structural_cases50_normal_seeded_ends_no_relative_or_predicate.json')
    end_adapter=read(previous)['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__);exec(compile(end_adapter,__file__+'::original-normal-value-carry','exec'),env)
    ends=[env['end_case'](arm,block,1514,p,s) for p in [0,1,2,3,0xFFFFFFFF] for s in [0,1,2,3,0xFFFFFFFF]]
    assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends) and not ctx.machines
    effects=[c for c in commands if c['word']!=0x4000];assert len(effects)==9 and sum(c['word']==0xA000 for c in effects)==1
    save(ROOT/'source_EV0_entry37_commands28_speeches_no_relative_predicate25_seeded_ends.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),
        current_ROM=inp['current_ROM'],current_ROM_sha256=inp['current_ROM_sha256'],current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),
        original_EV0_entry=entry,all_source_commands=commands,original_nontext_commands=effects,normal_seeded_ends=ends,source_macro_counts=counts,
        clean_andcurrent_source_owned_decoder_andentry_spans_equal=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        all37_original_commands28_complete_preambles_andseparate_terminal_tail_bound=True,
        no_relative_sites_or_raw_predicates_queries_in_this_source_block=True,
        native_EV0_entry_not_outer_eligibility_scheduler_or_natural_event50_activation=True,
        original_4821_at244_A000_at340_4720_at348_4681_at1510_bytes_andextents_preserved=True,
        full_item_effect_resource_camera_bodies_andnatural_context_not_claimed_executed=True,
        item_pigment_identity_FA_FI_getters_title_meaning_andcurrent_English_comparison_pending=True,
        known_names_reused_lead_not_new_B50_name_font_oractual_approval=True,
        source_owned_native_entry_adapter=adapter,source_owned_inventory_walker=walker,source_owned_inventory_function=inventory_source,source_owned_seeded_end_adapter=end_adapter,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,INPUT,previous,Path(__file__)]}))
    print('B50 source:original EV0entry,37commands/28speeches,zero relative/predicate/query sites,25seeded value-carry ends pass. Item/effects/macros/context/current English pending;zero credit.')
