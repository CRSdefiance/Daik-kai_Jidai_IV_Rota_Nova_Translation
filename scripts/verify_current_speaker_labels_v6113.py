"""Bind the user's earlier couple-label example to the current cumulative ROM."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/current_speaker_labels_v6113')
if __name__=='__main__':
    assert not ROOT.exists()
    release=read('work/analysis/shachihoko_release_v6111/registered_release_verification.json')
    target=NdsImage.open(release['candidate']);arm=target.read_file('/__arm9__.bin')
    parent=NdsImage.open('out/all_routes_combined_v6050_candidate.nds').read_file('/__arm9__.bin')
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']
    assert all(arm[0x120B80+i*32:0x120B80+i*32+12]==parent[0x120B80+i*32:0x120B80+i*32+12] for i in range(207))
    payload=bytes(MainCodeFile(arm,0x02000000).sections[3].data);oldpayload=bytes(MainCodeFile(parent,0x02000000).sections[3].data)
    allfields=[]
    for i in range(207):
        for delta in [0,4,8]:
            field=0x120B80+i*32+delta;ptr=struct.unpack_from('<I',arm,field)[0]
            if not ptr:continue
            if 0x02387A20<=ptr<0x02387A20+123040:
                at=ptr-0x02387A20;end=payload.index(0,at)+1;data=payload[at:end]
                assert data==oldpayload[at:end]
                allfields.append(dict(actor_ID=i,field_delta=delta,pointer_field=field,pointer=ptr,terminated_hex=data.hex()))
    manuscript=Path('translations/generic_speaker_labels_manuscript_v2.json');doc=read(manuscript);rows=[]
    for r in doc['records']:
        ident=int(r['id'].split('_')[1]);field=0x120B80+ident*32;ptr=struct.unpack_from('<I',arm,field)[0];at=ptr-0x02387A20
        text=payload[at:payload.index(0,at)].decode('ascii');assert text==r['english']
        rows.append(dict(actor_ID=ident,source_Japanese=r['source_Japanese'],current_label=text,current_reference=dict(file_path='/__arm9__.bin',pointer_field=field,runtime_pointer=ptr,payload_offset=at),contextual_reason=r['localization_note']))
    ROOT.mkdir(parents=True)
    save(ROOT/'existing_Man_Woman_Stranger_labels_and_broader_name_scope.json',dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],ARM9_sha256=sha(arm),source_manuscript=str(manuscript),source_manuscript_sha256=sha(manuscript.read_bytes()),current_labels=rows,all621_actor_name_pointer_fields_equal_V6050=True,all_referenced_staged_name_strings_equal_V6050=True,staged_fields=allfields,initial_three_label_changes_already_integrated_in_V5891=True,broader207_proper_names_roles_aliases_and_retrospective_consumers_still_open=True,approved_Rafael_Hodram_Joakim_Maria_Camille_preserved=True,user_screenshot_is_historical_evidence_not_current_gameplay=True,new_current_name_getter_or_GPU_execution=False,new_ROMs=0,new_emulator_runs=0,new_name_or_dialogue_completion_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Current V6110 primary labels:Man,Woman,Stranger. All621 name fields and referenced staged strings equal V6050;207-entry review remains open.')
