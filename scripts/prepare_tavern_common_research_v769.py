"""Full32 prose packing proof; production parser/registry/ROM stay unchanged."""

import inspect
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import tavern_conversations_editorial as original
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.review_tavern_continuation_v768 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_runtime_v769')
CURRENT=Path('out/all_routes_combined_v767_candidate.nds')


def main():
    native=read(ROOT/'full_output_verification.json');runtime=read(ROOT/'owned_runtime_plan.json')
    assert native['new32_complete_scoped_outputs']==14282 and not native['immutable_storage_writes']
    assert native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    rom=NdsImage.open(CURRENT);common=rom.read_file('/COMMON/MESFILE.DK4')
    arm=(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm)==runtime['target_ARM9_sha256']
    source=inspect.getsource(original.plan)
    replacements={'2 <= e.block <= 20':'2 <= e.block <= 23',
        'list(range(164, 1977))':'list(range(164, 2315))',
        'range(2, 21)':'range(2, 24)','len(groups) == 19':'len(groups) == 22'}
    for old,new in replacements.items():
        assert source.count(old) in(1,2),(old,source.count(old))
        source=source.replace(old,new)
    ns=dict(original.__dict__);ns['IDS']=tuple(range(851,883))
    exec(compile(source,str(Path(__file__)),'exec'),ns)
    doc=read(MANUSCRIPT);authored={r['message_id']:b' '+r['english'].removesuffix('{PAD}').encode('ascii') for r in doc['records']}
    for row in doc['records']:
        assert row['english'].removesuffix('{PAD}')==' '.join(row['english'].removesuffix('{PAD}').split())
    c,a,fields,mapping=ns['plan'](common,arm,authored)
    digest=sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    # A local exact-digest parser instance proves the prospective map. This does
    # not change the production whitelist or its source-bound code/table locks.
    local=dict(parser.__dict__)
    local['RELOCATED_DIRECTORY_HASHES']=parser.RELOCATED_DIRECTORY_HASHES|{digest}
    exec(compile(inspect.getsource(parser.common_message_entries),str(Path(parser.__file__)),'exec'),local)
    before=parser.common_message_entries(common,rom.read_file('/__arm9__.bin'),clean=False)
    after=local['common_message_entries'](c,a,clean=False)
    assert len(after)==3668
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    old_blocks,new_blocks=[IlnkContainer.parse(value).blocks for value in(common,c)]
    assert len(old_blocks)==len(new_blocks)==41
    assert all(x==y for i,(x,y) in enumerate(zip(old_blocks,new_blocks,strict=True)) if i not in range(2,24))
    opaque=[]
    for n in(1854,1865):
        x,y=before[n],after[n]
        old=old_blocks[x.block][x.block_offset:x.copy_end];new=new_blocks[y.block][y.block_offset:y.copy_end]
        assert old==new
        opaque.append({'id':n,'entire_native_copy_span_hex':old.hex()})
    restored=bytearray(a)
    for at,length in fields:restored[at:at+length]=arm[at:at+length]
    assert bytes(restored)==arm and max(map(len,new_blocks[2:24]))<=4096
    (ROOT/'COMMON_RESEARCH_ONLY.bin').write_bytes(c)
    (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').write_bytes(a)
    (ROOT/'prospective_plan_RESEARCH_ONLY.py').write_text(source,encoding='utf-8')
    save(ROOT/'prospective_common_repack.json',{'source_ROM_sha256':sha(CURRENT.read_bytes()),
        'source_COMMON_sha256':sha(common),'source_ARM9_sha256':sha(rom.read_file('/__arm9__.bin')),
        'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),'directory_sha256':digest,
        'metadata_fields':fields,'complete2151_selection_map':mapping,
        'selected32':sorted(authored),'all3636_unselected_visible_strings_byte_exact':True,
        'all19_unselected_blocks_byte_exact':True,'two_opaque_whole_copy_spans':opaque,
        'all41_blocks_retained_maximum4096_existing_cache_limits_preserved':True,
        'prior19_block_fit_exceeded_by_eight_messages261bytes_and20_21_block_extensions_still_spilled':True,
        'source_plan_module_sha256':sha(Path(original.__file__).read_bytes()),
        'effective_plan_sha256':sha(source.encode('utf-8')),'production_parser_sha256_unchanged':sha(Path(parser.__file__).read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_parser_registry_ROM_or_completion_change':True})
    print(f'All32 paragraphs fit existing blocks2-23;2151 whole selections,3636 unchanged strings,19 unchanged blocks. Exact research directory:{digest}.',flush=True)


if __name__=='__main__':main()
