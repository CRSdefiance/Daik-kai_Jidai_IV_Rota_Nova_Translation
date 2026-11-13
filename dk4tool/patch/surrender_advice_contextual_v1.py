"""One source-locked advisory-tone correction after the full V2284 stack."""
from pathlib import Path
import struct
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries,DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.verify_village_wrap_v608 import read

CONFIG='translations/surrender_advice_contextual_release_v1.json'
PATH='/COMMON/MESFILE.DK4'
IDS=[*range(1994,2011),*range(2022,2038),2192]

def current_entries(common,arm):
    conf=read(CONFIG)
    if (sha(common),sha(arm))==(conf['target_COMMON_sha256'],conf['target_ARM9_sha256']):
        return owned_entries(common,arm,conf['directory_sha256'])
    return previous_entries(common,arm)

def apply_release(candidate,baseline,path=CONFIG):
    conf=read(path);assert conf['format']=='dk4-surrender-advice-contextual-v1'
    for name,digest in conf['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    arm,common=candidate.read_file('/__arm9__.bin'),candidate.read_file(PATH)
    assert sha(arm)==conf['source_ARM9_sha256'] and sha(common)==conf['source_COMMON_sha256']
    assert sha(baseline.read_file(PATH))==conf['canonical_COMMON_sha256']
    doc=read(conf['manuscript']);validate_natural_dialogue_batch(doc)
    assert not doc['formatting_review_pending'] and doc['revised_IDs']==[2029] and doc['retained_count']==33
    assert [r['message_id'] for r in doc['records']]==IDS and doc['all34_native_previews_viewed_on_four_sheets']
    clean=NdsImage.open('work/clean.nds');assert sha(Path('work/clean.nds').read_bytes())==doc['source_ROM_sha256']
    jp=common_message_entries(clean.read_file(PATH),clean.read_file('/__arm9__.bin'))
    canonical=common_message_entries(baseline.read_file(PATH),baseline.read_file('/__arm9__.bin'),clean=False)
    before=previous_entries(common,arm);fonts=read(conf['native_proof']);plan=read(conf['payload_plan'])
    assert fonts['manuscript_sha256']==plan['manuscript_sha256']==doc['prior_contextual_draft_sha256']
    assert len(fonts['cases'])==712 and len(fonts['complete_native_planes'])==34 and fonts['findings']==[]
    assert len(plan['native_cold_warm_copies_all123_repacked_records'])==246
    authored={}
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    for row in doc['records']:
        n=row['message_id'];value=compiled(row)
        assert row['source_hex']==jp[n].text.hex() and row['canonical_source_hex']==canonical[n].text.hex()
        assert row['source_reference']==ref(jp[n]) and row['current_reference']==ref(before[n])
        assert row['current_hex']==before[n].text.hex() and row['proposed_compiled_hex']==value.hex()
        assert all(c['compiled_hex']==value.hex() for c in fonts['cases'] if c['message_ID']==n)
        if n==2029:
            assert row['editorial_decision']=='revise' and row['english']=='You cannot win! I suggest you surrender at once!'
            assert value!=before[n].text;authored[n]=value
        else:assert value==before[n].text and row['editorial_decision']=='retain-wording' and row['fresh_retained_wording_justification']
    source=IlnkContainer.parse(common);blocks=list(source.blocks);target=bytearray(arm);members=[r.message_id for r in before if r.block==22]
    assert members==list(range(1977,2100));body=bytearray();patches=[]
    def put(at,value):
        old=bytes(target[at:at+len(value)])
        if old!=value:patches.append(dict(address=0x02000000+at,offset=at,source_hex=old.hex(),target_hex=value.hex()));target[at:at+len(value)]=value
    for n in members:
        r=before[n];payload=source.blocks[22][r.block_offset:r.copy_end];assert payload.startswith(r.text+b'\0')
        if n in authored:payload=authored[n]+b'\0'
        put(TABLE_OFFSET+2*n,struct.pack('<H',len(body)));body.extend(payload)
    assert len(body)==5392 and len(source.blocks[22])==5378
    put(DIRECTORY_OFFSET+4*22,struct.pack('<HH',1977,len(body)))
    assert patches==plan['all_ARM9_changes_are_declared_directory_or_offset_metadata']
    blocks[22]=bytes(body);newcommon=IlnkContainer(blocks).to_bytes();newarm=bytes(target)
    assert sha(newcommon)==conf['target_COMMON_sha256']==plan['target_COMMON_sha256']
    assert sha(newarm)==conf['target_ARM9_sha256']==plan['target_ARM9_sha256']
    assert sha(newarm[DIRECTORY_OFFSET:TABLE_OFFSET])==conf['directory_sha256']
    after=owned_entries(newcommon,newarm,conf['directory_sha256']);assert len(after)==len(before)==3668
    for old,new in zip(before,after,strict=True):
        assert new.text==authored.get(old.message_id,old.text)
        if old.message_id not in authored:assert source.blocks[old.block][old.block_offset:old.copy_end]==blocks[new.block][new.block_offset:new.copy_end]
    assert all(a==b for i,(a,b) in enumerate(zip(source.blocks,blocks,strict=True)) if i!=22)
    restored=bytearray(newarm)
    for p in patches:at=p['offset'];restored[at:at+len(bytes.fromhex(p['source_hex']))]=bytes.fromhex(p['source_hex'])
    assert bytes(restored)==arm
    assert plan['new2029_loaded_template_hex']==authored[2029].hex()
    assert plan['new2029_complete_source_selected_direct_actor_loader_printf_macro_wrap_pipeline']['formatted_hex']==next(c['formatted_hex'] for c in fonts['complete_native_planes'] if c['message_ID']==2029)
    candidate.replace_file(PATH,newcommon);candidate.replace_file('/__arm9__.bin',newarm)
    return dict(manuscript=conf['manuscript'],source_ARM9_sha256=sha(arm),source_COMMON_sha256=sha(common),
        target_ARM9_sha256=sha(newarm),target_COMMON_sha256=sha(newcommon),directory_sha256=conf['directory_sha256'],
        reviewed_native_IDs=IDS,changed_records=[dict(id='COMMON_MESSAGE_2029')],actual_text_changed_IDs=[2029],
        changed_block=22,block_growth=14,metadata_patches=patches,all3667_other_complete_native_copies_and40_other_blocks_exact=True,
        all_other_ARM9_bytes_restore_exact_no_code_font_geometry_or_runtime_change=True,
        native_name_matrix_cases=712,complete_native_font_planes=34,repacked_cold_warm_copies=246,
        representative_and_registered_startup_completion_separate=True,full_goal_complete=False)
