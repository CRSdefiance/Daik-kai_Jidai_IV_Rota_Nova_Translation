"""Bind all clean B198 name fields without treating native fit as editorial approval."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_source_names_v5711')
NAMES=Path('work/analysis/lil_B198_names_v5707/four_original_progressive_and_catalogue_name_consumers.json')
VOICE=Path('work/analysis/lil_B198_voices_v5703/current207_catalog_eight_voices_and_two_source_selectors.json')
if __name__=='__main__':
    assert not ROOT.exists()
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    names,voice=read(NAMES),read(VOICE)
    expected={12:['ユキヒサ','シラキ','ゲンジョウ'],15:['アンジェロ','プッチーニ',None]}
    rows=[]
    for ident,values in expected.items():
        first=0x122000+(ident-164)*32
        fields=[]
        for delta,value in zip([0,4,8],values,strict=True):
            field=first+delta;pointer=struct.unpack_from('<I',clean,field)[0]
            if value is None:
                assert pointer==0;fields.append(dict(pointer_field=field,null=True));continue
            at=pointer-0x02000000;raw=clean[at:clean.index(0,at)+1]
            assert raw[:-1].decode('cp932')==value
            fields.append(dict(pointer_field=field,pointer=pointer,source_storage_offset=at,terminated_hex=raw.hex(),Japanese=value))
        rows.append(dict(actor_ID=ident,source_file='/__arm9__.bin',source_fields=fields,
            current_progressive_name=names['progressive_nameplate_values'][str(ident)],
            current_catalogue_name=names['full_catalogue_values'][str(ident)]))
    assert [(r['current_progressive_name'],r['current_catalogue_name']) for r in rows]==[
        ('Yukihisa Shiraki','Yukihisa Genjo Shiraki'),('Angelo Puccini','Angelo Puccini')]
    ROOT.mkdir(parents=True)
    save(ROOT/'two_actors_all_clean_fields_and_current_consumers.json',dict(source_name_records=rows,
        candidate=voice['candidate'],candidate_sha256=voice['candidate_sha256'],
        existing_proper_names_retained_pending_complete_contextual_editorial_review=True,
        no_new_kinship_rank_age_biography_or_relationship_inferred=True,
        third_field_not_an_invented_spoken_title=True,native_fit_proofs_not_fresh_name_localization_credit=True,
        evidence={str(p):sha(p.read_bytes()) for p in [NAMES,VOICE,Path(__file__)]},new_ROMs=0,new_review_credit=0,full_goal_complete=False))
    print('B198 all five non-null Japanese name fields and one null bound to both current consumers. No editorial completion credit.')
