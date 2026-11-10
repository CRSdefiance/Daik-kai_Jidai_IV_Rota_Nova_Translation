"""Bind original630B request,A000 structure and full normal end without forcing game state."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B225_controls_v7181');SOURCE=Path('work/analysis/lil_B225_source_v7178/thirteen_clean_current_children_heroes_exchange_source_references.json');INPUT=Path('work/analysis/current_V7168_native_v7173/current_native_input.json');SEEDED=Path('work/analysis/lil_B212_seeded_ends_v6634/150_native_terminal_seed_cases_normal_residual_and_flagged_zero.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);spec=packet['blocks'][0];assert packet['source_relative_sites']==packet['source_typed_commands']==packet['source_C200']==0 and packet['source_630B']==packet['source_A000']==1
    adapter=read(SEEDED)['source_owned_adapter'];env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::source-normal-end','exec'),env);structural=[];ends=[];leaves=[]
    for label,path,key in [('clean-Japanese','work/clean.nds','all_clean_native_commands'),('current-English',packet['current_ROM'],'all_current_native_commands')]:
        im=NdsImage.open(path);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[225];commands=spec[key]
        assert len(block)==976 and 8+struct.unpack_from('<H',block,4)[0]==974 and block[970:]==bytes(6) and len(commands)==16
        other=[c for c in commands if c['word']!=0x4000];assert [(c['offset'],c['whole_command_hex'],c['native_extent']) for c in other]==[(78,'0b63',2),(962,'00a0ffff48000110',8),(970,'00000000',4)];leaves.append(dict(version=label,non_speech_commands=other))
        for c in other[:-1]:
            raw=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;r=walk(arm,isolated);assert r['error'] is None and r['stopped_offset']==r['logical_end']==len(isolated) and len(r['rows'])==1 and r['rows'][0]['word']==c['word'] and r['rows'][0]['native_extent']==c['native_extent'];structural.append(dict(version=label,original_offset=c['offset'],word=c['word'],source_command_hex=raw.hex(),**r))
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for seed in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,**env['end_case'](arm,block,970,previous,seed)))
    for a,b in zip(structural[:2],structural[2:],strict=True):assert a['rows']==b['rows'] and a['opaque_effect_bridges']==b['opaque_effect_bridges'] and a['source_command_hex']==b['source_command_hex']
    assert len(ends)==50 and all(not e['flagged_terminal'] and e['native_result'][0]==0 and e['native_result'][1]==e['initial_value_word'] for e in ends)
    text=checked_text(inspect.getsource(resource_base.control630A),{"value=bytes.fromhex('0a63')":"value=bytes.fromhex('0b63')",'[0x02386EFC,10,2,1]':'[0x02386EFC,11,2,1]'})
    native=dict(resource_base.__dict__);exec(compile(text,__file__+'::source630B','exec'),native);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');resources=[]
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for result in [0,0xFFFFFFFF]:resources.append(ctx.execute(native['control630A'],previous,result));ctx.machines.pop()
    assert len(resources)==10 and not ctx.machines and all(r['all4MiB_owner_input_ABI_output_and_length_guards_exact'] for r in resources)
    save(ROOT/'four_source630B_A000_structural10_resource50_normal_end_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source630B_A000_structural_cases=structural,source_current_three_exact_non_speech_leaves=leaves,source630B_boundary_cases=resources,source630B_request_args=[0x02386EFC,11,2,1],source630B_resource_body_unexecuted_no_role_assignment_in_original_decoder=True,source630B_not_automatic_evidence_of_sound_or_full_callee_semantics=True,normal_terminal_seed_cases=ends,normal_state0_retains_seeded_value_in_all50_cases=True,source_stored976_logical974_tail2_complete_end970_preserved=True,opaque_A000_effect_bodies_bridged_not_fully_explained=True,source_owned_adapters=dict(source630B=text,seeded_end=adapter),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_gameplay_result_role_roster_funds_RNG_or_event_flags_forced=True,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,SEEDED,Path(resource_base.__file__),Path(__file__)]},full_goal_complete=False));print('B225:original630B request[owner,11,2,1],10 unchanged-memory resource boundaries,4 source/current630B/A000 structural cases,50 normal ends. No role assignment orfull resource-body claim;zero credit.')
