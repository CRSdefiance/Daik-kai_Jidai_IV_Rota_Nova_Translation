"""Bind C200's current fleet-derived descriptor field, not a historical constant."""
from pathlib import Path
import inspect
from scripts.prove_lil_B139_C200_v3461e import C200 as original_C200
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B190_C200_v5318')
SOURCE=Path('work/analysis/lil_B190_source_v5314/all17_clean_current_complete_context.json')


def adapter_source():
    source=inspect.getsource(original_C200).replace('def C200(','def current_C200(')
    needle='    ui=struct.unpack_from'
    assert source.count(needle)==1
    source=source.replace(needle,"    fleet_root=get(0xCB1A8);fleet_index=get(0x2E58C);fleet_object=fleet_root+4+fleet_index*0x84\n    direct=get(0x34674,fleet_object);expected_owner=cpu.mem_read(fleet_object+0x3C,1)[0] if direct==0x73 else direct\n    ctor=[]\n"+needle)
    needle="    hs.append(cpu.hook_add(UC_HOOK_CODE,entry,begin=BASE+0x21B80,end=BASE+0x21B80))"
    assert source.count(needle)==1
    source=source.replace(needle,needle+"\n    hs.append(cpu.hook_add(UC_HOOK_CODE,lambda u,p,s,d:ctor.append(dict(descriptor=u.reg_read(UC_ARM_REG_R0),source_owner=u.reg_read(UC_ARM_REG_R1),mode=u.reg_read(UC_ARM_REG_R2))),begin=BASE+0x904CC,end=BASE+0x904CC))")
    needle="    expected_words=[descriptor[1],descriptor[2],descriptor[3],descriptor[4],descriptor[5],descriptor[6],1]"
    assert source.count(needle)==1
    source=source.replace(needle,"    assert len(ctor)==1 and ctor[0]==dict(descriptor=descriptors[0]['descriptor'],source_owner=expected_owner,mode=13)\n    assert descriptor[2]==expected_owner\n"+needle)
    needle='return dict(offset=command'
    assert source.count(needle)==1
    source=source.replace(needle,"return dict(original_fleet_source=dict(root=fleet_root,index=fleet_index,object=fleet_object,direct_owner_result=direct,selected_descriptor_value=expected_owner,source73_fallback_used=direct==0x73),original_constructor=ctor[0],offset=command")
    return source


_namespace=dict(original_C200.__globals__)
exec(compile(adapter_source(),__file__+'::source-fleet-provenance','exec'),_namespace)
C200=_namespace['current_C200']

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B190_voices_v5315/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    c=next(c for c in packet['blocks'][0]['all_current_native_commands'] if c['word']==0xC200);rows=[]
    for label,path in [('clean','work/clean.nds'),('current',packet['current_ROM'])]:
        block=IlnkContainer.parse(NdsImage.open(path).read_file('/data/SC2.DK4')).blocks[190]
        rows.append(dict(version=label,**ctx.execute(C200,block,c)));ctx.machines.pop()
    assert not ctx.machines
    assert rows[0]['source_owned_UI_request_words']==rows[1]['source_owned_UI_request_words']==[1,2,13,0,0,0,1]
    assert rows[0]['source_owned_UI_writes']==rows[1]['source_owned_UI_writes']
    save(ROOT/'source_fleet_descriptor_two_C200_contracts.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),cases=rows,source_owned_adapter=adapter_source(),
        descriptor_value2_is_original_current_fleet_getter_input_not_an_invented_constant=True,
        historical_London_descriptor_value0_not_assumed_for_current_opening=True,
        native_presentation_resource_bodies_still_explicitly_unexecuted=True,
        all_other4MiB_native_state_and_ABI_exact=True,actual_B190_transition_not_observed=True,
        no_actor_rank_or_relationship_inferred_from_UI_owner_value=True,new_review_credit=0,full_goal_complete=False))
    print('Both C200 contracts pass:original fleet-derived value2,mode13,exact owned writes;all other4MiB preserved.')
