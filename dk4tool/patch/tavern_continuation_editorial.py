"""Source-locked Tavern851-882 English,full region phrases and scoped runtime."""

import struct
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import tavern_continuation_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET,common_message_entries
from scripts.review_tavern_continuation_v768 import ARGUMENTS
from scripts.verify_village_wrap_v608 import read

IDS=tuple(range(851,883))
RESEARCH=Path('work/analysis/tavern_runtime_v769')


def compile_text(row):
    n,text=row['message_id'],row['english'].removesuffix('{PAD}')
    if (n not in IDS or not text or len(text)>=200 or text!=' '.join(text.split()) or not text.isascii()
            or any(ord(c)<32 or ord(c)>=127 for c in text) or any(c in text for c in '{}')):
        raise ValueError('One ordinary ASCII paragraph without authored alignment or breaks required')
    indices=[1,0] if n==878 else [0] if n in(871,872) else list(range(len(ARGUMENTS.get(n,[]))))
    if row['source_native_arguments']!=ARGUMENTS.get(n,[]) or row['English_argument_source_indices']!=indices:
        raise ValueError('Native argument identities/order or reviewed gendered-address omission differs')
    if text.count('%s')!=len(indices) or '%' in text.replace('%s',''):
        raise ValueError('Every reviewed printed argument must occur exactly once')
    return b' '+text.encode('ascii')


def runtime_transform(arm):
    assert sha(arm)==runtime.SOURCE
    proof=read(RESEARCH/'owned_runtime_plan.json')
    assert proof['runtime_module_sha256']==sha(Path(runtime.__file__).read_bytes())
    assert proof['all_active_prefixes_and_all8_short_UI_names_and_geometry_exact']
    assert proof['all_selected_tails_have_zero_absolute_branch_ADR_crossing_string_references']
    assert proof['all_section_sizes_autoload_ITCM_pool_cache_geometry_preserved']
    result=bytearray(arm);blobs=runtime.assemble(arm)
    assert {p['address']:bytes.fromhex(p['target_hex']) for p in proof['patches']}==blobs
    for p in proof['patches']:
        at=p['address']-runtime.BASE;before,after=bytes.fromhex(p['source_hex']),bytes.fromhex(p['target_hex'])
        assert arm[at:at+len(before)]==before
        result[at:at+len(after)]=after
    result=bytes(result)
    assert sha(result)==proof['target_ARM9_sha256'] and cache_plan(result)==cache_plan(arm)
    return result,proof


def transform(common,arm,manuscript):
    assert manuscript['translation_policy']=='natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records'])==IDS
    assert sha(arm)==runtime.SOURCE
    clean,canonical=[NdsImage.open(p) for p in('work/clean.nds','out/raphael_natural_v2_accepted_base.nds')]
    path='/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path))==manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path))==manuscript['source_canonical_COMMON_sha256']
    source=common_message_entries(clean.read_file(path),clean.read_file('/__arm9__.bin'))
    accepted=common_message_entries(canonical.read_file(path),canonical.read_file('/__arm9__.bin'),clean=False)
    before=common_message_entries(common,arm,clean=False);authored={}
    for row in manuscript['records']:
        n=row['message_id']
        assert source[n].text.hex()==row['source_hex'] and accepted[n].text.hex()==row['canonical_source_hex']
        assert before[n].text.hex()==row['current_text_hex']
        assert source[n].text.count(b'%s')==len(ARGUMENTS.get(n,[]))
        authored[n]=compile_text(row)
    patched,proof=runtime_transform(arm)
    c,a,fields,mapping=plan(common,patched,authored)
    after=common_message_entries(c,a,clean=False)
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    old,new=[IlnkContainer.parse(value).blocks for value in(common,c)]
    assert all(x==y for i,(x,y) in enumerate(zip(old,new,strict=True)) if i not in range(2,24))
    for n in(1854,1865):
        x,y=before[n],after[n]
        assert old[x.block][x.block_offset:x.copy_end]==new[y.block][y.block_offset:y.copy_end]
    restored=bytearray(a)
    for at,length in fields:restored[at:at+length]=patched[at:at+length]
    assert bytes(restored)==patched and cache_plan(a)==cache_plan(arm)
    return c,a,{'changed_records':[f'COMMON_MESSAGE_{n}' for n in IDS],
        'owned_runtime':proof,'metadata_fields':fields,'complete2151_selection_map':mapping,
        'all3636_other_visible_strings_and19_other_blocks_exact':True,
        'all8_UI_region_names_and_metadata_unchanged_private_full_dialogue_regions':True,
        'two_opaque_native_copy_spans_preserved_byte_exact':[1854,1865],
        'experimental':True,'actual_gameplay_pending':True}


def apply_release(common,arm,path):
    config=read(path)
    assert config['format']=='dk4-tavern-continuation-editorial-v1'
    assert sha(common)==config['source_common_sha256'] and sha(arm)==config['source_arm9_sha256']
    for p,h in config['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    doc=Path(config['manuscript']);assert sha(doc.read_bytes())==config['manuscript_sha256']
    c,a,proof=transform(common,arm,read(doc))
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256']
    return c,a,proof


def plan(common, arm, authored):
    assert tuple(sorted(authored)) == IDS
    before = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    selected = [e for e in before if 2 <= e.block <= 23]
    assert [e.message_id for e in selected] == list(range(164, 2315))
    opaque = {}
    for e in selected:
        tail = blocks[e.block][e.block_offset + len(e.text) + 1:e.copy_end]
        if set(tail) - {0, 32}:
            assert e.message_id in (1854, 1865) and e.message_id not in authored
            opaque[e.message_id] = blocks[e.block][e.block_offset:e.copy_end]
    assert set(opaque) == {1854, 1865}
    for k in range(2, 24):
        first = next(e for e in selected if e.block == k)
        assert set(blocks[k][:first.block_offset]) <= {0, 32}
    groups, group, body = [], [], bytearray()
    for entry in selected:
        text = opaque.get(entry.message_id, authored.get(entry.message_id, entry.text) + b'\0')
        if len(body) + len(text) > 4096:
            groups.append((group, bytes(body))); group, body = [], bytearray()
        group.append((entry.message_id, len(body), text)); body.extend(text)
    groups.append((group, bytes(body)))
    assert len(groups) == 22
    rebuilt, target, fields, mapping = list(blocks), bytearray(arm), [], []
    for block, (group, raw) in zip(range(2, 24), groups, strict=True):
        rebuilt[block] = raw
        at = DIRECTORY_OFFSET + block * 4
        struct.pack_into('<HH', target, at, group[0][0], len(raw)); fields.append((at, 4))
        for n, offset, text in group:
            at = TABLE_OFFSET + n * 2
            struct.pack_into('<H', target, at, offset); fields.append((at, 2))
            mapping.append({'id': n, 'block': block, 'offset': offset,
                            'text_hex': authored.get(n, before[n].text).hex(), 'complete_payload_hex': text.hex()})
    return IlnkContainer(rebuilt).to_bytes(), bytes(target), fields, mapping
