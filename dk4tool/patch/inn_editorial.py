"""Registered source-locked Inn prose and exact existing-allocation runtime."""

import struct
from pathlib import Path
from types import FunctionType,SimpleNamespace

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import palace_label_boundaries as previous
from dk4tool.patch import inn_editorial_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.prepare_item_common_v788 import repack
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_village_wrap_v608 import read

ROOT=Path('work/analysis/inn_integration_v803')
IDS=tuple(range(1177,1200))
SOURCE_ARM='9fbf8f0e8ea7e9f82d697a1938bbda7dd170bf5d15976f9334c995335e78b8e1'
SOURCE_COMMON='24e0c9e280f1352581a5758f672e85c779d6290e8ff2ceeab14345578a4ad20f'


def compiled(row):
    text=row['english'].removesuffix('{PAD}')
    assert row['message_id'] in IDS and text==' '.join(text.split()) and text.isascii()
    assert all(32<=ord(c)<127 for c in text) and not any(c in text for c in '{}')
    argc=len(row['source_native_arguments'])
    assert text.count('%s')==argc and '%' not in text.replace('%s','')
    assert row['English_argument_source_indices']==list(range(argc))
    return b' '+text.encode('ascii')


def plan(common,arm,rows):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    authored={r['message_id']:compiled(r) for r in rows};assert tuple(authored)==IDS
    scoped=SimpleNamespace(common_message_entries=lambda c,a,clean=False:previous.current_entries(c,a))
    pack=FunctionType(repack.__code__,{**repack.__globals__,'parser':scoped})
    before,blocks,first,last,selected,opaque,groups,attempts=pack(common,arm,authored)
    patched=runtime.apply(arm);target=bytearray(patched);rebuilt=list(blocks);fields=[]
    for block,(group,body) in zip(range(first,last+1),groups,strict=True):
        rebuilt[block]=body;at=parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH',target,at,group[0][0],len(body));fields.append((at,4))
        for n,offset,payload in group:
            at=parser.TABLE_OFFSET+n*2;struct.pack_into('<H',target,at,offset);fields.append((at,2))
    c,a=IlnkContainer(rebuilt).to_bytes(),bytes(target)
    directory=sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    after=local_entries(directory)(c,a,clean=False)
    assert len(after)==len(before)==3668
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    assert all(blocks[n]==rebuilt[n] for n in range(len(blocks)) if not first<=n<=last)
    for n,payload in opaque.items():
        e=after[n];assert rebuilt[e.block][e.block_offset:e.copy_end]==payload
    restored=bytearray(a)
    for at,size in fields:restored[at:at+size]=patched[at:at+size]
    assert bytes(restored)==patched and cache_plan(a)==cache_plan(arm)
    old_code,new_code=[MainCodeFile(v,0x02000000) for v in (arm,a)]
    shape=lambda code:[(s.ramAddress,len(s.data),s.bssSize) for s in code.sections]
    assert shape(old_code)==shape(new_code) and bytes(old_code.sections[3].data)==bytes(new_code.sections[3].data)
    assert len(new_code.sections[3].data)-48==123040
    assert all(after[n].text==before[n].text for n in (346,347,348,676,677))
    previous.verify_final(a)
    return c,a,dict(changed_records=[f'COMMON_MESSAGE_{n}' for n in IDS],directory_sha256=directory,
        metadata_fields=fields,repacked_block_range=[first,last],packing_attempts=attempts,
        all3645_unselected_strings_exact=True,complete_opaque_payloads_and_unselected_blocks_exact=True,
        sections_BSS_cache_and_staged123040_bytes_exact=True,
        source_COMMON_sha256=sha(common),source_ARM9_sha256=sha(arm),target_COMMON_sha256=sha(c),target_ARM9_sha256=sha(a),
        source_owned_168_byte_runtime_and52_byte_strings_no_growth=True,experimental=True,full_goal_complete=False)


def current_entries(common,arm):
    cfg=read('translations/inn_editorial_release_v1.json')
    assert sha(common)==cfg['target_common_sha256'] and sha(arm)==cfg['target_arm9_sha256']
    return local_entries(cfg['directory_sha256'])(common,arm,clean=False)


def apply_release(common,arm,path):
    cfg=read(path);assert cfg['format']=='dk4-inn-editorial-v1'
    assert sha(common)==cfg['source_common_sha256']==SOURCE_COMMON and sha(arm)==cfg['source_arm9_sha256']==SOURCE_ARM
    for p,h in cfg['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    manuscript=Path(cfg['manuscript']);assert sha(manuscript.read_bytes())==cfg['manuscript_sha256']
    doc=read(manuscript);validate_natural_dialogue_batch(doc)
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    time_path=Path(cfg['time_manuscript']);assert sha(time_path.read_bytes())==cfg['time_manuscript_sha256']
    time_doc=read(time_path);validate_natural_dialogue_batch(time_doc)
    assert [r['english'] for r in time_doc['records']]==['Last month','This month','%s months ago']
    assert all(all(r['review'][g] for g in ('source','context','localization','naturalness','formatting')) for r in time_doc['records'])
    draft_path=Path(doc['reviewed_research_manuscript']);assert sha(draft_path.read_bytes())==doc['reviewed_research_manuscript_sha256']
    draft=read(draft_path)
    keys=lambda rows:[(r['message_id'],r['english'],r['source_meaning']) for r in rows]
    assert keys(doc['records'])==keys(draft['records'])
    clean,canonical=[NdsImage.open(p) for p in ('work/clean.nds','out/raphael_natural_v2_accepted_base.nds')]
    jp=parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    accepted=parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    prior=previous.current_entries(common,arm)
    for r in doc['records']:
        n=r['message_id'];assert r['source_hex']==jp[n].text.hex()
        assert r['canonical_source_hex']==accepted[n].text.hex() and r['current_text_hex']==prior[n].text.hex()
        assert all(r['review'][g] for g in ('source','context','localization','naturalness','formatting'))
    c,a,proof=plan(common,arm,doc['records'])
    assert sha(c)==cfg['target_common_sha256'] and sha(a)==cfg['target_arm9_sha256']
    native=read(ROOT/'production_layout.json')
    assert native['ARM9_sha256']==sha(a) and native['COMMON_sha256']==sha(c)
    assert native['native_layouts']==1169 and native['full_font_planes']==96 and not native['findings']
    scope=read('work/analysis/inn_runtime_v802/scope_proof.json')
    assert scope['cases']==35320 and scope['new_ordinary_IDs']==list(runtime.ORDINARY) and scope['new_yes_no_IDs']==list(runtime.YES_NO)
    assert scope['new_queued_ordinary_tables']==[0x021180E0]
    assert read('work/analysis/inn_runtime_v802/status_contracts.json')['count']==140
    assert read('work/analysis/inn_runtime_v802/complete_month_phrases.json')['count']==144
    entries=local_entries(proof['directory_sha256'])(c,a,clean=False)
    first,last=proof['repacked_block_range']
    copies=[read(ROOT/f'native_copies/native_copies_block_{b:02d}.json') for b in range(first,last+1)]
    assert {(r['message_id'],r['cold_cache']) for p in copies for r in p['cases']}=={(e.message_id,cold) for e in entries if first<=e.block<=last for cold in (False,True)}
    assert all(p['COMMON_sha256']==sha(c) and p['ARM9_sha256']==sha(a) for p in copies)
    assert all(r['complete_native_copy']['entire_native_span_including_post_NUL_payload_exact'] for p in copies for r in p['cases'])
    return c,a,proof
