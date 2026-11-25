"""Source-locked courier status paragraphs and bounded modal wrapper extension."""

import struct
from pathlib import Path
from types import FunctionType, SimpleNamespace

from keystone import KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import captain_prompt_wrap as modal
from dk4tool.patch import item_diplomacy_editorial as previous
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.prepare_item_common_v788 import repack
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_village_wrap_v608 import read

ROOT=Path('work/analysis/arrival_notices_v792')
IDS=(346,347,348)
SOURCE_ARM='4c2e19d9834bfa79a5e90897afe7c3332f4c850077f2db4c5eb57949f57217bd'
SOURCE_COMMON='5fbacd4b1c6041e280c72aee4f8caf1ccf201911892150d8b09ffde1a24ebca5'


def modal_code():
    address=modal.ADDRESS
    stub=bytes(Ks(KS_ARCH_ARM,KS_MODE_ARM).asm(f'ldr ip,[pc];bx ip;.word {address+13}',address)[0])
    text='''push {r4-r6,lr}
movs r6,#0
ldr r3,[sp,#0xd4]
ldr r4,parent
cmp r3,r4
bne fallback
ldr r3,[sp,#0xe0]
subs r3,#127
cmp r3,#7
bls active
subs r3,#142
cmp r3,#3
bls active
subs r3,#52
cmp r3,#0
beq active
cmp r3,#6
beq active
subs r3,#25
cmp r3,#2
bhi fallback
movs r6,#1
active:
sub sp,#248
mov r4,r0
blx 0x02053914
mov r0,r4
add r1,sp,#8
movs r3,#0
str r3,[sp]
cmp r6,#0
bne balanced
blx 0x01ffca00
b wrapped
balanced:
bl 0x02147ae4
wrapped:
cmp r0,#0
beq done
adds r2,r0,#1
mov r0,r4
add r1,sp,#8
blx 0x020cec74
done:
movs r0,#0
add sp,#248
pop {r4-r6,pc}
fallback:
pop {r4-r6}
pop {r3}
mov lr,r3
ldr r3,original
bx r3
.align 2
parent: .word 0x020546e8
original: .word 0x01ff9ce4
'''
    body=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(text,address+12)[0])
    assert len(stub)==12 and len(stub)+len(body)<=modal.SIZE
    result=stub+body
    assert len(result)%2==0
    return result+bytes.fromhex('c046')*((modal.SIZE-len(result))//2),text


def runtime_transform(arm):
    assert sha(arm)==SOURCE_ARM
    code=MainCodeFile(arm,0x02000000)
    section=code.sections[4];assert section.ramAddress==0x01FFC000 and len(section.data)==4096
    off=modal.ADDRESS-section.ramAddress
    old=bytes(Ks(KS_ARCH_ARM,KS_MODE_ARM).asm(modal.ASM,modal.ADDRESS)[0])
    assert bytes(section.data[off:off+modal.SIZE])==old
    section.data[off:off+modal.SIZE]=modal_code()[0]
    target=bytes(code.save());assert cache_plan(target)==cache_plan(arm)
    return target


def compiled(row):
    text=row['english'].removesuffix('{PAD}')
    assert row['message_id'] in IDS and text==' '.join(text.split()) and text.isascii()
    assert all(32<=ord(c)<127 for c in text) and not any(c in text for c in '{}')
    assert text.count('%s')==1 and '%' not in text.replace('%s','')
    assert row['English_argument_source_indices']==[0]
    return b' '+text.encode('ascii')


def plan(common,arm,rows):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    authored={r['message_id']:compiled(r) for r in rows}
    assert tuple(authored)==IDS
    scoped=SimpleNamespace(common_message_entries=lambda c,a,clean=False:previous.current_entries(c,a))
    pack=FunctionType(repack.__code__,{**repack.__globals__,'parser':scoped})
    before,blocks,first,last,selected,opaque,groups,attempts=pack(common,arm,authored)
    patched=runtime_transform(arm);target=bytearray(patched);rebuilt=list(blocks);fields=[]
    for block,(group,body) in zip(range(first,last+1),groups,strict=True):
        rebuilt[block]=body;at=parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH',target,at,group[0][0],len(body));fields.append((at,4))
        for n,offset,payload in group:
            at=parser.TABLE_OFFSET+n*2;struct.pack_into('<H',target,at,offset);fields.append((at,2))
    c,a=IlnkContainer(rebuilt).to_bytes(),bytes(target)
    directory=sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    after=local_entries(directory)(c,a,clean=False)
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    assert all(blocks[n]==rebuilt[n] for n in range(len(blocks)) if not first<=n<=last)
    for n,payload in opaque.items():
        e=after[n];assert rebuilt[e.block][e.block_offset:e.copy_end]==payload
    restored=bytearray(a)
    for at,size in fields:restored[at:at+size]=patched[at:at+size]
    assert bytes(restored)==patched
    original_code,target_code=[MainCodeFile(v,0x02000000) for v in (arm,a)]
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in original_code.sections]==[(s.ramAddress,len(s.data),s.bssSize) for s in target_code.sections]
    assert bytes(original_code.sections[3].data)==bytes(target_code.sections[3].data)
    assert len(target_code.sections[3].data)-48==123040
    return c,a,{'changed_records':[f'COMMON_MESSAGE_{n}' for n in IDS],'metadata_fields':fields,
        'directory_sha256':directory,'repacked_block_range':[first,last],'packing_attempts':attempts,
        'only_three_logical_strings_changed_all3665_other_strings_exact':True,
        'opaque_payloads_unselected_blocks_sections_BSS_cache_and_staged123040_bytes_unchanged':True,
        'modal_wrapper_owned_existing128_bytes':[modal.ADDRESS,modal.ADDRESS+modal.SIZE],
        'experimental':True,'full_goal_complete':False}


def current_entries(common,arm):
    cfg=read('translations/arrival_notices_editorial_release_v1.json')
    assert sha(common)==cfg['target_common_sha256'] and sha(arm)==cfg['target_arm9_sha256']
    return local_entries(cfg['directory_sha256'])(common,arm,clean=False)


def apply_release(common,arm,path):
    cfg=read(path);assert cfg['format']=='dk4-arrival-notices-editorial-v1'
    assert sha(common)==cfg['source_common_sha256'] and sha(arm)==cfg['source_arm9_sha256']
    for name,h in cfg['dependencies'].items():assert sha(Path(name).read_bytes())==h,name
    manuscript=Path(cfg['manuscript']);assert sha(manuscript.read_bytes())==cfg['manuscript_sha256']
    doc=read(manuscript);validate_natural_dialogue_batch(doc)
    assert doc['translation_policy']=='natural-dialogue-v2'
    draft_path=Path(doc['reviewed_research_manuscript'])
    assert sha(draft_path.read_bytes())==doc['reviewed_research_manuscript_sha256']
    draft=read(draft_path)
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in draft['records']]
    native=read(ROOT/'native_verification.json');consumer=read(ROOT/'consumer_proof.json')
    assert native['manuscript_sha256']==sha(draft_path.read_bytes()) and native['exact_modal_scope_added']==list(IDS)
    assert native['all_other3665_IDs_byte_exact'] and len(native['wrong_parent_controls'])==84
    assert len(native['layouts'])==49 and all(not r['findings'] for r in native['layouts'])
    assert len(native['complete_font_planes'])==7 and len(consumer['rows'])==3
    visual=read(ROOT/'visual_review.json');assert visual['preview_sha256']==native['preview_sha256'] and visual['all_seven_planes_visually_reviewed']
    clean,canonical=[NdsImage.open(p) for p in ('work/clean.nds','out/raphael_natural_v2_accepted_base.nds')]
    jp=parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    accepted=parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    old=previous.current_entries(common,arm)
    for r in doc['records']:
        n=r['message_id'];assert jp[n].text.hex()==r['source_hex'] and accepted[n].text.hex()==r['canonical_source_hex'] and old[n].text.hex()==r['current_text_hex']
    c,a,proof=plan(common,arm,doc['records'])
    assert sha(c)==cfg['target_common_sha256'] and sha(a)==cfg['target_arm9_sha256']
    assert native['research_ARM9_sha256']==consumer['ARM9_sha256']==sha(a)
    copies=[read(ROOT/f'native_copies/native_copies_block_{b:02d}.json') for b in range(6)]
    entries=local_entries(proof['directory_sha256'])(c,a,clean=False)
    assert {(r['message_id'],r['cold_cache']) for p in copies for r in p['cases']}=={(e.message_id,cold) for e in entries if e.block<=5 for cold in (False,True)}
    assert all(p['COMMON_sha256']==sha(c) and p['ARM9_sha256']==sha(a) for p in copies)
    assert all(r['complete_native_copy']['entire_native_span_including_post_NUL_payload_exact'] for p in copies for r in p['cases'])
    return c,a,proof
