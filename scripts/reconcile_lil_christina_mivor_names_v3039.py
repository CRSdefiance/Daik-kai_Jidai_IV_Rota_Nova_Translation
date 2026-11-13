"""Current registered actor catalog and contextual identity reconciliation."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Christina_Mivor_names_v3039')
SOURCE=Path('work/analysis/lil_Christina_Mivor_source_v3035/complete145_clean_current_native_context.json')
def names(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(0x02000000,0x400000));root=get(0xCB184);assert get(0x7F244)==2
    results=[]
    for ident in [6,7,79,162,167]:
        actor=root+4+32*ident;vt=struct.unpack('<I',cpu.mem_read(actor,4))[0];fn=struct.unpack('<I',cpu.mem_read(vt+8,4))[0]
        ptr=get(fn-0x02000000,actor);value=bytes(cpu.mem_read(ptr,80)).split(b'\0')[0].decode('cp932')
        results.append(dict(actor_ID=ident,actor_object=actor,getter=fn,pointer=ptr,current_catalog_name=value))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(rows=results,all_actor_models_and_unowned4MiB_exact=True,current_executed_instruction_addresses=len(provider.executed_current))
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_Christina_Mivor_controls_v3037/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context');result=ctx.execute(names);ctx.machines.pop();assert not ctx.machines
    byid={r['actor_ID']:r for r in result['rows']};assert byid[79]['current_catalog_name']=='Mivor Genz' and byid[162]['current_catalog_name']=='Boy' and byid[167]['current_catalog_name']=='Lady'
    save(ROOT/'current_registered_names_and_source_identity_contract.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),**result,
        Mivor_full_name='Mivor Genz',provisional_source_packet_Gentz_annotation_superseded_not_original_Japanese=True,
        approved_Christina_spelling_retained_legacy_Cristina_catalog_not_edited=True,Julio_biological_grandfather_source_B72_R0176=True,
        Boy_FE_source_visible_label='Boy:',Boy_and_mother_actor162_167_and_nonkinship_familiar_addresses=True,
        registered_name_config=source['registered_name_catalog_config'],registered_name_config_sha256=source['registered_name_catalog_config_sha256'],
        no_new_nameplate_observation_or_name_asset_change=True,new_emulator_runs=0,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(current_catalog={i:r['current_catalog_name'] for i,r in byid.items()},all_unowned_state_exact=True,no_editorial_credit=True))
