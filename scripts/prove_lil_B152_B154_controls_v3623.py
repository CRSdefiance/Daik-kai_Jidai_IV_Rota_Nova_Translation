"""Bind two unforced crew predicates,three C200s,five picture/hide sites,pause andseven630x values."""
import inspect
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.map_lil_B122_B127_source_v3260c import control2000
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B152_B154_controls_v3623')
SOURCE=Path('work/analysis/lil_B152_B154_source_v3619/all59_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in images];words=sorted({c['word'] for g in packet['blocks'] for c in g['all_current_native_commands'] if c['word']&0xFF00==0x6300});assert words==[0x630B,0x6325,0x6328,0x6329,0x632A,0x632B,0x632C];text=inspect.getsource(resource_base.control630A);changes=[('previous,boundary_return):','previous,boundary_return,word):'),("value=bytes.fromhex('0a63')","assert word in SOURCE_RESOURCE_WORDS;value=struct.pack('<H',word)"),('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]
    for a,b in changes:assert a in text,a;text=text.replace(a,b)
    env={**resource_base.__dict__,'SOURCE_RESOURCE_WORDS':words};exec(compile(text,str(Path(__file__))+'::seven_source630x','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B152_B160_voices_v3616/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');predicates=[];uis=[];pictures=[];resources=[];pause=[];opaque=[]
    for g in packet['blocks']:
        n=g['block']
        for c in g['all_current_native_commands']:
            if c['word']==0x8000:
                r=ctx.execute(probe,blocks[1][n],c);ctx.machines.pop();assert not r['original_event_completion_calls'];predicates.append(dict(block=n,**r))
            elif c['word'] in [0xC200,0x4821,0x4822,0x4823,0x4700]:
                values=[]
                for version,bs in zip(['clean','current'],blocks,strict=True):r=ctx.execute(C200 if c['word']==0xC200 else picture,bs[n],c);ctx.machines.pop();values.append(dict(version=version,**r))
                if c['word']==0xC200:assert values[0]['source_owned_UI_writes']==values[1]['source_owned_UI_writes'] and values[0]['source_owned_UI_request_words']==values[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1];uis.append(dict(block=n,source_offset=c['offset'],cases=values))
                else:assert values[0]['original_picture_boundary_calls']==values[1]['original_picture_boundary_calls'];pictures.append(dict(block=n,word=c['word'],source_offset=c['offset'],cases=values))
            elif c['word']==0x2000:
                assert n==154;values=control2000(images[1].read_file('/__arm9__.bin'),c);assert len(values)==10;pause.append(dict(block=n,source_offset=c['offset'],source_command_hex=c['whole_command_hex'],next_source_instruction_offset=c['offset']+c['native_extent'],cases=values,source_current_bytes_exact=True,source_resume_mapping_must_follow_relocation=True))
            elif c['word'] not in [0x4000,0x100,0x200,0x300,0x400] and c['word']&0xFF00!=0x6300:opaque.append(dict(block=n,offset=c['offset'],word=c['word'],source_current_hex=c['whole_command_hex'],preserved_by_exact_leaf_ownership_not_full_effect_execution=True))
    for word in words:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:resources.append(ctx.execute(env['control630A'],previous,result,word));ctx.machines.pop()
    assert len(predicates)==2 and len(uis)==3 and len(pictures)==5 and len(pause)==1 and len(resources)==70 and not ctx.machines;assert packet['source_relative_sites']==8;save(ROOT/'two_predicates_three_C200_five_pictures_pause_and70_resource_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=predicates,source_C200_pairs=uis,source_picture_pairs=pictures,source2000_pause_and_resume=pause,source630x_resource_words=words,source630x_boundary_cases=resources,other_opaque_source_current_controls=opaque,source_owned_adapters=dict(predicate=inspect.getsource(probe),C200=inspect.getsource(C200),picture=inspect.getsource(picture),control2000=inspect.getsource(control2000),source630x=text),all_control_leaves_already_exact_in_342_packet=True,source45FF_46xx_6008_05xx_and_five_A000_effects_preserve_byte_ownership_not_full_effect_execution=True,all_UI_pause_picture_resource_bodies_explicit_unexecuted=True,no_actual_eligibility_gameplay_earned_recruitment_or_item_outcome=True,all_eight_source_relative_sites_bound_separately_by80_native_cases=True,scope_packet_relative_sites8_initial_success_stdout_literal9_was_stale_only=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B152_B154_IDs=[],new_emulator_runs=0,no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(unforced_predicates=[(r['source_command_hex'],r['native_result']) for r in predicates],C200_pairs=3,picture_pairs=5,pause_cases=10,resource_cases=70,source_relative_sites=8,body_execution_and_gameplay_not_claimed=True,credit=0))
