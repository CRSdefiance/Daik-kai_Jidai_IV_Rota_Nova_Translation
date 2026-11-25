"""Source-locked recruitment prose,typed condition phrases and exact reblocking."""

from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import recruitment_editorial_runtime as runtime
from dk4tool.patch import tavern_continuation_editorial as previous
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read

IDS=tuple(range(883,908))
RESEARCH=Path('work/analysis/recruitment_owned_v772')
ARGUMENTS={**{n:['native_gold_cost'] for n in range(890,897)},904:['native_number_gathered'],
    905:['town_name','native_city_status_label'],906:['town_name','native_city_status_label']}


def compile_text(row):
    n,text=row['message_id'],row['english'].removesuffix('{PAD}')
    if (n not in IDS or not text or len(text)>=200 or text!=' '.join(text.split()) or not text.isascii()
            or any(ord(c)<32 or ord(c)>=127 for c in text) or any(c in text for c in '{}')):
        raise ValueError('One ordinary ASCII paragraph without alignment or authored breaks required')
    arguments=ARGUMENTS.get(n,[])
    if row['source_native_arguments']!=arguments or row['English_argument_source_indices']!=list(range(len(arguments))):
        raise ValueError('Exact native argument identities and order required')
    if text.count('%s')!=len(arguments) or '%' in text.replace('%s',''):
        raise ValueError('Every native argument must occur exactly once')
    return b' '+text.encode()


def runtime_transform(arm):
    assert sha(arm)==runtime.SOURCE
    proof=read(RESEARCH/'owned_runtime_plan.json')
    assert proof['source_ARM9_sha256']==runtime.SOURCE and proof['all_section_pool_cache_BSS_geometry_preserved']
    closure=read(RESEARCH/'quantity_caller_closure.json')
    assert len(closure['exact_seven_ARM_BLs'])==7
    assert not any(closure[k] for k in('absolute_aliases','external_ADR_leads','external_Thumb_BL_BLX_leads'))
    assert not read(RESEARCH/'storage_reference_census.json')['unexpected_references']
    blobs=runtime.assemble()
    assert blobs=={r['address']:bytes.fromhex(r['target_hex']) for r in proof['patches']}
    code=MainCodeFile(arm,runtime.BASE)
    for row in proof['patches']:
        section=code.sections[row['section']];at=row['address']-section.ramAddress
        old,new=bytes.fromhex(row['source_hex']),bytes.fromhex(row['target_hex'])
        assert bytes(section.data[at:at+len(old)])==old
        section.data[at:at+len(new)]=new
    target=bytes(code.save());assert sha(target)==proof['target_ARM9_sha256']
    assert cache_plan(target)==cache_plan(arm) and len(target)==len(arm)
    return target,proof


def plan(common,arm,authored):
    env=dict(previous.__dict__);env['IDS']=IDS
    return FunctionType(previous.plan.__code__,env)(common,arm,authored)


def transform(common,arm,manuscript):
    assert manuscript['translation_policy']=='natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records'])==IDS
    assert sha(arm)==runtime.SOURCE
    consumer=read(manuscript['consumer_routing_proof'])
    assert consumer['original_source_callers_select_nonnull_portrait_core_for_this_family']
    assert len(consumer['all114_immutable_city_cultures_and_role13_mappings'])==114
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
        'all3643_other_strings_and19_other_blocks_exact':True,'opaque_whole_copy_spans_preserved':[1854,1865],
        'registered_experimental_actual_gameplay_pending':True}


def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-recruitment-editorial-v1'
    assert sha(common)==config['source_common_sha256'] and sha(arm)==config['source_arm9_sha256']
    for p,h in config['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    doc=Path(config['manuscript']);assert sha(doc.read_bytes())==config['manuscript_sha256']
    c,a,proof=transform(common,arm,read(doc))
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256']
    return c,a,proof
