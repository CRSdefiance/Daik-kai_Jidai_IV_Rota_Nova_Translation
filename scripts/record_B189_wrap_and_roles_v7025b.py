"""Preserve exact whole-exchange wrap and occupational-name leads without new approval."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/B189_retrospective_wrap_and_roles_v7025b')
SCOPE=Path('work/analysis/square_shopkeeper_scope_v6972/ten_source_identical_roles_current_owners_alias_fields_and_whole_clean_story_contexts.json')
FIXTURE=Path('work/analysis/square_shopkeeper_scenes_v7022/four_complete_static_staged_nameplate_fixtures.json')
NAMES=Path('work/analysis/square_shopkeeper_names_v7021/all_name_field_voice_dynamic_macro_and_complete_native_label_consumers.json')
if __name__=='__main__':
    assert not ROOT.exists();scope,fixture,names=map(read,[SCOPE,FIXTURE,NAMES])
    source=next(c for c in scope['story_contexts'] if c['file_path']=='/data/SC2.DK4' and c['block']==189)
    current=next(f for f in fixture['fixtures'] if f['case']=='static_parent');clean=NdsImage.open('work/clean.nds');parent=NdsImage.open(fixture['parent'])
    jp,arm=[i.read_file('/__arm9__.bin') for i in [clean,parent]];sourcebody=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[189]
    body=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks[189]
    assert sha(sourcebody)==source['source_block_sha256'] and sha(body)==current['source_block_sha256']
    rows=[]
    for a,b in zip(source['whole_clean_transcript'],current['original_text_records'],strict=True):
        assert a['source_selector']==b['source_selector'];raw=bytes.fromhex(b['current_text_hex']);at=b['fixture_command_offset']-48+5
        assert body[at:at+len(raw)+1]==raw+b'\0'
        rows.append(dict(source_id=f'DK4_MES_B189_R{a["source_reference"]["record_index"]:04d}',source_reference=a['source_reference'],source_hex=a['source_hex'],Japanese=a['Japanese'],
            current_probe_id=b['id'],current_reference=dict(block=189,offset=at,bytes=len(raw),header_offset=at-5,record_index=body[:at].count(b'\0')),
            current_hex=raw.hex(),current_stored_English=raw[1:].decode('ascii'),current_row_lengths=[len(s) for s in raw[1:].decode('ascii').splitlines()],
            source_selector=a['source_selector'],fresh_whole_exchange_prose_and_wrap_review_pending=True,new_review_credit=0))
    assert len(rows)==17 and rows[0]['current_stored_English'].startswith('I finally got hold ')
    byid={r['actor_ID']:r['text'] for r in names['versions'][0]['name_getters']['rows'] if r['consumer']=='progressive-nameplate'}
    source_names={}
    for ident in range(207):
        field=0x120B80+ident*32;p=struct.unpack_from('<I',jp,field)[0]
        if not p:continue
        at=p-0x02000000;end=jp.index(0,at);source_names[ident]=dict(actor_ID=ident,pointer_field=field,source_pointer=p,source_storage_offset=at,Japanese=jp[at:end].decode('cp932'),source_terminated_hex=jp[at:end+1].hex(),current_English=byid[ident])
    groups={}
    for ident in [104,113,147]:groups[str(ident)]=[v for v in source_names.values() if v['Japanese']==source_names[ident]['Japanese']]
    ROOT.mkdir(parents=True);save(ROOT/'whole_B189_exact_wrap_refs_and_three_occupational_name_groups_pending.json',dict(file_path='/data/SC2.DK4',block=189,
        source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),source_block_sha256=sha(sourcebody),
        current_ROM=fixture['parent'],current_ROM_sha256=fixture['parent_sha256'],current_block_sha256=sha(body),records=rows,
        concrete_wrap_finding='The first existing paragraph splits after I finally got hold,well before the native36-cell row limit. Review the complete17-speech exchange and its authored early rows as a retrospective layout/prose batch;do not silently revise it inside the name-data layer.',
        exact_clean_occupational_groups=groups,
        role_review_finding='104 clean交易所の親父/currentTrader and113 clean出港所の兄貴/currentPort Worker need whole shared/caller/context review.親父/兄貴 are familiar occupational labels here,not proof of father/brother relationships. Do not invent kinship,rank,manual-labor duties or a formal office title.147 cleanギルドの元締め supports the meaning of currentGuildmaster,but this nameplate test does not globally approve that group.',
        source_whole_context6974_preceded_current_prose_fixture_reading=True,previous_source_role_only_reading_not_new_prose_approval=True,
        all17_body_bytes_preserved_in_current_name_research=True,nameplate_GPU_capture_not_a_fresh17_record_editorial_pass=True,
        all207_name_queue_and_retrospective_wrapping_scope_remain_open=True,no_proposed_global_name_replacement=True,new_review_credit=0,new_ROMs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SCOPE,FIXTURE,NAMES,Path(__file__)]},full_goal_complete=False))
    print(dict(B189_complete_pending_records=17,related_role_group_sizes={k:len(v) for k,v in groups.items()},new_credit=0),flush=True)
