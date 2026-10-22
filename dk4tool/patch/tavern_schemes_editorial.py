"""Source-locked scheme prose and exact private-table routing."""

from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import tavern_continuation_editorial as previous
from dk4tool.patch import tavern_schemes_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries,DIRECTORY_OFFSET,TABLE_OFFSET
import struct
from scripts.verify_village_wrap_v608 import read

IDS=tuple(range(908,964))
ROOT=Path('work/analysis/tavern_schemes_integration_v776')
ARGUMENTS={**{n:['scheme_label'] for n in range(915,921)},
    **{n:['faction','town'] for n in range(940,948)},
    **{n:['first_faction','second_faction'] for n in range(948,956)},
    **{n:['town','faction'] for n in range(956,964)}}


def compile_text(row):
    n=row['message_id']
    text=row['english'].removesuffix('{PAD}')
    if (n not in IDS or not text or len(text)>=200 or text!=' '.join(text.split())
            or not text.isascii() or any(ord(c)<32 or ord(c)>=127 for c in text)
            or any(c in text for c in '{}')):
        raise ValueError('One ordinary ASCII paragraph without authored breaks or alignment required')
    args=ARGUMENTS.get(n,[])
    if row['source_native_arguments']!=args or row['English_argument_source_indices']!=list(range(len(args))):
        raise ValueError('Original scheme argument identities and order required')
    if text.count('%s')!=len(args) or '%' in text.replace('%s',''):
        raise ValueError('Each original scheme argument must occur exactly once')
    return b' '+text.encode()


def runtime_transform(arm):
    assert sha(arm)==runtime.SOURCE
    refs=read(ROOT/'current_storage_references.json')
    assert refs['source_ARM9_sha256']==runtime.SOURCE and not refs['unexpected']
    plan=read('work/analysis/tavern_scheme_selector_v775/two_patch_plan.json')
    assert plan['source_ARM9_sha256']==runtime.SOURCE
    assert runtime.code()=={r['address']:bytes.fromhex(r['target_hex']) for r in plan['patches']}
    code=MainCodeFile(arm,0x02000000)
    for row in plan['patches']:
        off=row['address']-code.sections[0].ramAddress
        old,new=bytes.fromhex(row['source_hex']),bytes.fromhex(row['target_hex'])
        assert code.sections[0].data[off:off+len(old)]==old
        assert len(new)<=row['existing_owned_capacity']
        code.sections[0].data[off:off+len(new)]=new
    target=bytes(code.save())
    assert sha(target)==plan['target_ARM9_sha256']
    assert len(target)==len(arm) and cache_plan(target)==cache_plan(arm)
    return target,plan


def plan(common,arm,authored):
    assert tuple(sorted(authored))==IDS
    before=common_message_entries(common,arm,clean=False)
    blocks=IlnkContainer.parse(common).blocks
    selected=[e for e in before if 2<=e.block<=29]
    assert [e.message_id for e in selected]==list(range(164,2861))
    opaque={}
    for e in selected:
        tail=blocks[e.block][e.block_offset+len(e.text)+1:e.copy_end]
        if set(tail)-{0,32}:
            assert e.message_id in (1854,1865) and e.message_id not in authored
            opaque[e.message_id]=blocks[e.block][e.block_offset:e.copy_end]
    assert set(opaque)=={1854,1865}
    for k in range(2,30):
        first=next(e for e in selected if e.block==k)
        assert set(blocks[k][:first.block_offset])<={0,32}
    groups=[]
    group=[]
    body=bytearray()
    for e in selected:
        payload=opaque.get(e.message_id,authored.get(e.message_id,e.text)+b'\0')
        if len(body)+len(payload)>4096:
            groups.append((group,bytes(body)))
            group=[]
            body=bytearray()
        group.append((e.message_id,len(body),payload))
        body.extend(payload)
    groups.append((group,bytes(body)))
    assert len(groups)==28
    rebuilt=list(blocks)
    target=bytearray(arm)
    fields=[]
    mapping=[]
    for block,(group,raw) in zip(range(2,30),groups,strict=True):
        assert len(raw)<=4096
        rebuilt[block]=raw
        at=DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH',target,at,group[0][0],len(raw))
        fields.append((at,4))
        for n,offset,payload in group:
            at=TABLE_OFFSET+n*2
            struct.pack_into('<H',target,at,offset)
            fields.append((at,2))
            mapping.append({'id':n,'block':block,'offset':offset,
                'text_hex':authored.get(n,before[n].text).hex(),'complete_payload_hex':payload.hex()})
    return IlnkContainer(rebuilt).to_bytes(),bytes(target),fields,mapping


def transform(common,arm,manuscript):
    assert manuscript['translation_policy']=='natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records'])==IDS
    assert sha(arm)==runtime.SOURCE
    contract=read(manuscript['input_contract'])
    assert contract['editable_company_name_does_not_reach_these_original_scheme_consumers']
    assert contract['all39730_fixed_catalog_layouts_are_clean']
    clean,canonical=[NdsImage.open(p) for p in ('work/clean.nds','out/raphael_natural_v2_accepted_base.nds')]
    path='/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path))==manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path))==manuscript['source_canonical_COMMON_sha256']
    source=common_message_entries(clean.read_file(path),clean.read_file('/__arm9__.bin'))
    accepted=common_message_entries(canonical.read_file(path),canonical.read_file('/__arm9__.bin'),clean=False)
    before=common_message_entries(common,arm,clean=False)
    authored={}
    for row in manuscript['records']:
        n=row['message_id']
        assert source[n].text.hex()==row['source_hex']
        assert accepted[n].text.hex()==row['canonical_source_hex']
        assert before[n].text.hex()==row['current_text_hex']
        assert source[n].text.count(b'%s')==len(ARGUMENTS.get(n,[]))
        authored[n]=compile_text(row)
    patched,proof=runtime_transform(arm)
    c,a,fields,mapping=plan(common,patched,authored)
    after=common_message_entries(c,a,clean=False)
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    old,new=[IlnkContainer.parse(v).blocks for v in (common,c)]
    assert all(x==y for i,(x,y) in enumerate(zip(old,new,strict=True)) if i not in range(2,30))
    for n in (1854,1865):
        x,y=before[n],after[n]
        assert old[x.block][x.block_offset:x.copy_end]==new[y.block][y.block_offset:y.copy_end]
    restored=bytearray(a)
    for at,size in fields:restored[at:at+size]=patched[at:at+size]
    assert bytes(restored)==patched and cache_plan(a)==cache_plan(arm)
    return c,a,{'changed_records':[f'COMMON_MESSAGE_{n}' for n in IDS],
        'private_runtime':proof,'metadata_fields':fields,'complete2697_selection_map':mapping,
        'all3612_other_strings_and13_other_blocks_exact':True,
        'opaque1854_1865_complete_native_payloads_exact':True,'experimental':True,'actual_gameplay_pending':True}


def apply_release(common,arm,path):
    cfg=read(path)
    assert cfg['format']=='dk4-tavern-schemes-editorial-v1'
    assert sha(common)==cfg['source_common_sha256'] and sha(arm)==cfg['source_arm9_sha256']
    for p,h in cfg['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    doc=Path(cfg['manuscript'])
    assert sha(doc.read_bytes())==cfg['manuscript_sha256']
    c,a,proof=transform(common,arm,read(doc))
    assert sha(c)==cfg['target_common_sha256'] and sha(a)==cfg['target_arm9_sha256']
    return c,a,proof
