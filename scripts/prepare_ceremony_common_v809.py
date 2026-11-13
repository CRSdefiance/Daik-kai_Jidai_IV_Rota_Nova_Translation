"""Pack the51 changed ceremony paragraphs into existing COMMON blocks;research."""

import struct
from pathlib import Path
from types import FunctionType,SimpleNamespace

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.inn_editorial import current_entries
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts import ceremony_runtime_v808 as runtime
from scripts.prepare_item_common_v788 import repack
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ceremony_integration_v809')
MANUSCRIPT=Path('translations/ceremony_editorial_manuscript_v2.json')
IDS=(289,290,291,293,294,295,*range(1200,1245))


def compiled(row):
    text=row['english'].removesuffix('{PAD}');n=row['message_id']
    assert n in IDS and text==' '.join(text.split()) and text.isascii()
    assert all(32<=ord(c)<127 for c in text) and not any(c in text for c in '{}')
    argc=len(row['source_native_arguments'])
    assert text.count('%s')==argc and '%' not in text.replace('%s','')
    assert row['English_argument_source_indices']==list(range(argc))
    return b' '+text.encode('ascii')


def plan(common,arm,rows):
    assert sha(arm)==runtime.SOURCE and sha(common)=='027e272120e9ce2a657ee3cd72490c4caae101af5c19b4427e75412766d93967'
    authored={r['message_id']:compiled(r) for r in rows if r['message_id']!=64}
    assert tuple(authored)==IDS
    scoped=SimpleNamespace(common_message_entries=lambda c,a,clean=False:current_entries(c,a))
    pack=FunctionType(repack.__code__,{**repack.__globals__,'parser':scoped})
    before,blocks,first,last,selected,opaque,groups,attempts=pack(common,arm,authored)
    patched=runtime.apply(arm);target=bytearray(patched);rebuilt=list(blocks);fields=[];mapping=[]
    for block,(group,body) in zip(range(first,last+1),groups,strict=True):
        rebuilt[block]=body;at=parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH',target,at,group[0][0],len(body));fields.append((at,4))
        for n,offset,payload in group:
            at=parser.TABLE_OFFSET+n*2;struct.pack_into('<H',target,at,offset);fields.append((at,2))
            mapping.append(dict(id=n,block=block,offset=offset,text_hex=authored.get(n,before[n].text).hex(),complete_payload_hex=payload.hex()))
    c,a=IlnkContainer(rebuilt).to_bytes(),bytes(target)
    directory=sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET]);after=local_entries(directory)(c,a,clean=False)
    assert len(after)==len(before)==3668
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    assert all(blocks[n]==rebuilt[n] for n in range(len(blocks)) if not first<=n<=last)
    for n,payload in opaque.items():
        e=after[n];assert rebuilt[e.block][e.block_offset:e.copy_end]==payload
    restored=bytearray(a)
    for at,size in fields:restored[at:at+size]=patched[at:at+size]
    assert bytes(restored)==patched and cache_plan(a)==cache_plan(arm)
    old_code,new_code=[MainCodeFile(v,runtime.BASE) for v in (arm,a)]
    shape=lambda code:[(s.ramAddress,len(s.data),s.bssSize) for s in code.sections]
    assert shape(old_code)==shape(new_code)
    assert all(bytes(old_code.sections[n].data)==bytes(new_code.sections[n].data) for n in (1,2,3))
    assert len(new_code.sections[3].data)-48==123040
    assert all(after[n].text==before[n].text for n in (64,292,346,347,348,676,677))
    return c,a,dict(source_COMMON_sha256=sha(common),source_ARM9_sha256=sha(arm),
        target_COMMON_sha256=sha(c),target_ARM9_sha256=sha(a),directory_sha256=directory,
        metadata_fields=fields,repacked_block_range=[first,last],packing_attempts=attempts,
        changed_records=[f'COMMON_MESSAGE_{n}' for n in IDS],
        all3617_other_messages_including_shared64_and_unrelated292_exact=True,
        complete_opaque_payloads_and_unselected_blocks_exact=True,
        sections_BSS_cache_staged123040_and_all_metadata_exceptions_verified=True,
        exact_relocation_map=mapping,full_goal_complete=False)


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    doc=read(MANUSCRIPT);rom=NdsImage.open(runtime.ROM)
    common,arm=rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    native=read(runtime.ROOT/'native_runtime_verification.json');modal=read(runtime.ROOT/'modal_scope.json')
    assert native['research_ARM9_sha256']==sha(runtime.apply(arm))
    assert modal['exact_six_new_modal_IDs']==list(runtime.MODAL_IDS)
    original=NdsImage.open('work/clean.nds')
    jp=parser.common_message_entries(original.read_file('/COMMON/MESFILE.DK4'),original.read_file('/__arm9__.bin'))
    en=current_entries(common,arm)
    for row in doc['records']:
        n=row['message_id'];assert jp[n].text.hex()==row['source_hex'] and en[n].text.hex()==row['current_text_hex']
        assert all(row['review'][g] for g in ('source','context','localization','naturalness'))
    c,a,proof=plan(common,arm,doc['records'])
    (ROOT/'COMMON_RESEARCH_ONLY.bin').write_bytes(c);(ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').write_bytes(a)
    proof.update(manuscript_sha256=sha(MANUSCRIPT.read_bytes()),source_Japanese_and_current51_exact=True,
        runtime_proof_sha256=sha((runtime.ROOT/'native_runtime_verification.json').read_bytes()),
        consumers_proof_sha256=sha((runtime.ROOT/'effective_consumer_formats.json').read_bytes()),
        new_ROM_or_completion_credit=False,producer_sha256=sha(Path(__file__).read_bytes()))
    save(ROOT/'prospective_common_repack.json',proof)
    save(ROOT/'complete_current_message_map_v809.json',dict(COMMON_sha256=sha(c),ARM9_sha256=sha(a),
        entries=[dict(message_id=e.message_id,block=e.block,block_offset=e.block_offset,copy_end=e.copy_end,
            table_offset=e.table_offset,text_hex=e.text.hex()) for e in local_entries(proof['directory_sha256'])(c,a,clean=False)]))
    print(f'51 ceremony paragraphs fit existing blocks{proof["repacked_block_range"]};3617 others and all opaque spans exact. COMMON {sha(c)};ARM9 {sha(a)}. Research only.',flush=True)


if __name__=='__main__':main()
