"""Read only clean-Japanese name fields for all B48 actors before current-English exposure."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_native_given_name_table import string
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_clean_names_v8021')
SOURCE=Path('work/analysis/Rafael_next_clean_v8020/complete_clean_SC0_B48_EV0_andcoverage_before_current_English.json')
if __name__=='__main__':
    assert not ROOT.exists()
    source=read(SOURCE);g=source['groups'][0];image=NdsImage.open(source['source_ROM']);arm=image.read_file('/__arm9__.bin')
    assert sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    table=struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000;assert table==0x120B80
    chosen=sorted({r['source_selector'] for r in g['records'] if r['source_selector']!=254})
    assert chosen==[0,4,5,6,7,8,13,75,113]
    rows=[]
    for ident in chosen:
        fields=[]
        for col,kind in [(0,'given'),(4,'surname'),(8,'middle')]:
            at=table+32*ident+col
            fields.append(dict(kind=kind,table_field=at,table_field_hex=arm[at:at+4].hex(),
                **string(arm,struct.unpack_from('<I',arm,at)[0])))
        rows.append(dict(source_actor_ID=ident,source_selector=f'{ident:02X}',fields=fields,
            source_speech_IDs=[r['id'] for r in g['records'] if r['source_selector']==ident],
            current_name_fields_getters_voices_full_consumers_andlocalization_not_yet_reviewed=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'nine_clean_static_identity_fields_before_current_English.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        clean_ARM9_sha256=sha(arm),table_field_source='Original ARM9 pointer0xCDAC0 and32-byte actor rows,as in prior immutable source-bound identity probes.',
        records=rows,FE_speech_IDs=[r['id'] for r in g['records'] if r['source_selector']==254],
        source_only_no_current_English_names_orbody_exposed=True,
        proper_names_roles_titles_hidden_identity_andcharacterization_to_review_in_full_exchange=True,
        new_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for r in rows:print(r['source_actor_ID'],[v.get('text') for v in r['fields']])
